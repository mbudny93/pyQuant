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

def insertQuotesIntoDB(con, quotes, dbname, symbol_table_name, price_table_name):
    for day in quotes.values:
        date, open, high, low, close = day
        print(date)
        time.sleep(0.001)

    columns = ''
    values = []
    query = ('INSERT INTO %s (%s) VALUES %s')%(price_table_name, columns, values)
    print(query)

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


