import pandas
import time
import pymysql

def establishConnection():
    connection = pymysql.connect(host='localhost', user='admin', password='admin')
    return connection

def closeConnection(connection):
    with connection.cursor() as cursor:
        cursor.close()
        connection.close()

def prepareInsertQuery(connection, quotes, dbname, symbol_table_name, price_table_name):
    return True

def getPriceTableColumns(connection, quotes, dbname, symbol_table_name, price_table_name):
    query = ('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE'
        '`TABLE_SCHEMA`=\'%s\' AND `TABLE_NAME`=\'%s\';')%(dbname, price_table_name)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result = result[1:]

    columns = ''
    for idx, column in enumerate(result):
        columns+=column[0]
        columns+=", "
    columns = columns[0:-2]
    return columns

def insertQuotesIntoDB(connection, quotes, dbname, symbol_table_name, price_table_name):
    columns = getPriceTableColumns(connection, quotes, dbname, symbol_table_name, price_table_name)
    preliminary_query = 'INSERT INTO %s (%s) VALUES '%(price_table_name, columns)

    for day in quotes.values:
        date, open, high, low, close = day
        values_query = '%s, %s, %s, %s, %s'%(str(date), str(open), str(high), str(low), str(close))
        query = preliminary_query + values_query
        print(query)
        time.sleep(0.001)

    # cursor = con.cursor()
    # cursor.execute(query)

dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'

quotes = pandas.read_csv('eurusd_d.csv')
quotes = quotes.tail(4000)

con = establishConnection()
insertQuotesIntoDB(con, quotes, dbname, symbol_table_name, price_table_name)
closeConnection(con)


