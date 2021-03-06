import pymysql
import sys;
import lxml.html
import datetime
import requests
import time
import pandas
from dataVendor import DataVendor, AlphaVantage, Quotemedia, Tiingo, Stooq

# DROP USER admin@localhost;
# CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
# GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';

def generateQueries(symbol_table_name, price_table_name):
    symbol_table = "CREATE TABLE `%s` (\
      `id` int NOT NULL AUTO_INCREMENT,\
      `ticker` varchar(32) NOT NULL,\
      `name` varchar(255) NULL,\
      `sector` varchar(255) NULL,\
      PRIMARY KEY (`id`)\
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"%symbol_table_name

    price_table = "CREATE TABLE `%s` (\
      `id` int NOT NULL AUTO_INCREMENT,\
      `price_date` datetime NOT NULL,\
      `open_price` decimal(19,4) NULL,\
      `high_price` decimal(19,4) NULL,\
      `low_price` decimal(19,4) NULL,\
      `close_price` decimal(19,4) NULL,\
      `volume` bigint NULL,\
      PRIMARY KEY (`id`)\
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"%price_table_name

    return symbol_table, price_table

def establishConnection():
    connection = pymysql.connect(host='localhost', user='admin', password='admin')
    return connection

def closeConnection(connection):
    with connection.cursor() as cursor:
        cursor.close()
        connection.close()

def createDB(connection, dbname):
    try:
        with connection.cursor() as cursor:
            query = 'create database %s;'%(dbname)
            cursor.execute(query)
            query = 'use %s;'%(dbname)
            cursor.execute(query)
        connection.commit()
        print('Database', dbname, 'succesfully created')
    finally:
        pass

def createTables(connection, symbol_table, price_table):
    try:
        with connection.cursor() as cursor:
            # print(symbol_table)
            cursor.execute(symbol_table)
            cursor.execute(price_table)

        connection.commit()
        print('Tables succesfully created')
    finally:
        pass

def dropDB(connection, dbname):
    try:
        with connection.cursor() as cursor:
            query = 'drop database %s;'%(dbname)
            cursor.execute(query)
        connection.commit()
    except:
        pass

def getTickers():
    now = datetime.datetime.utcnow()
    url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)

    tickers = html.xpath('//table[1]//td[1]//text()')[0:-1:2]
    securities = html.xpath('//table[1]//td[2]//text()')
    symbols = html.xpath('//table[1]//td[4]//text()')

    tuples = []
    for tick, comp, sym in zip(tickers, securities, symbols):
        tup = (tick, comp, sym, now)
        tuples.append(tup)
    print('Symbols succesfully generated')

    return tuples

def printTickers(tuples):
    for idx, tuple in enumerate(tuples):
        print(idx, tuple)

def insertSymbolsIntoDB(connection, tickers, dbname, symbol_table_name, price_table_name):
    query = 'SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`=\'%s\' AND `TABLE_NAME`=\'%s\';'%(dbname, symbol_table_name)

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result = result[1:]

    columns = ''
    for idx, column in enumerate(result):
        columns+=column[0]
        columns+=", "
    columns = columns[0:-2]

    for symbol in tickers:
        values = symbol[0:-1]
        query = 'INSERT INTO %s (%s) VALUES %s'%(symbol_table_name, columns, values)
        cursor.execute(query)
        connection.commit()
        print('Adding', symbol[1], '...')
    print('Database succesfully created.')

def fetchTickersFromDB(con, dbname, symbol_table_name):
    cursor = con.cursor()
    query = 'SELECT ticker FROM %s'%(symbol_table_name)
    cursor.execute(query)
    result = cursor.fetchall()

    tickerz = []
    for idx, tck in enumerate(result):
        tickerz.append(tck[0])
    return tickerz

############################################################################################

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

def insertQuotesIntoDB(connection, quotes, dbname, symbol_table_name, price_table_name, vendor):
    cursor = connection.cursor()
    columns = getPriceTableColumns(connection, quotes, dbname, symbol_table_name, price_table_name)
    preliminary_query = 'INSERT INTO %s (%s) VALUES '%(price_table_name, columns)

    for day in quotes.values:
        d, o, h, l, c, v = vendor.adapt(day)
        values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(d), str(o), str(h), str(l), str(c), str(v))
        query = preliminary_query + values_query
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        cursor.execute(query)
        # print(query)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    connection.commit()

def firstUpdate(con, tickerzFromDB, dbname, symbol_table_name, price_table_name, vendorName):
    dataVendor = DataVendor(vendorName)
    for ticker in tickerzFromDB:
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print('Fetching', ticker, 'historical quotes from', dataVendor.getVendorName(), 'database...')
        quotes = dataVendor.fetchQuotes(ticker)
        print(ticker, 'data collected. Adding to database...')
        insertQuotesIntoDB(con, quotes, dbname, symbol_table_name, price_table_name, dataVendor)
        print(ticker, 'datas inserted.')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
