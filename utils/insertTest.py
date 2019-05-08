import pymysql
import pandas
from dbCreator import *
from dataVendor import DataVendor, AlphaVantage, Quotemedia, Tiingo, Stooq
import sys
import math

def validate(tupleOfQuotes):
    cond = False
    for x in tupleOfQuotes:
        if x!=x:
            cond = True
    if cond:
        print('PRZYPAL')
    else:
        print('OK')

    return tupleOfQuotes

def debugz(connection, quotes, dbname, symbol_table_name, price_table_name, vendor):
    cursor = connection.cursor()
    columns = getPriceTableColumns(connection, quotes, dbname, symbol_table_name, price_table_name)
    preliminary_query = 'INSERT INTO %s (%s) VALUES '%(price_table_name, columns)
    quotes = quotes.dropna()

    for day in quotes.values:
        # d, o, h, l, c, v = vendor.adapt(day)
        dohlcv = vendor.adapt(day)
        # validate values
        d, o, h, l, c, v = validate(dohlcv)
        # validate values
        values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(d), str(o), str(h), str(l), str(c), str(v))
        query = preliminary_query + values_query
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # print(query)
        cursor.execute(query)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # connection.commit()

def debug(ticker):
    dbname = 'test'
    symbol_table_name = 'symbol'
    price_table_name = 'daily_price'
    data_vendor = 'quotemedia'
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tickers = getTickers()
    con = establishConnection()
    dropDB(con, dbname)
    createDB(con, dbname)
    symbol_table, price_table = generateQueries(symbol_table_name, price_table_name)
    createTables(con, symbol_table, price_table)
    insertSymbolsIntoDB(con, tickers, dbname, symbol_table_name, price_table_name)
    tickerzFromDB = fetchTickersFromDB(con, dbname, symbol_table_name)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    dataVendor = DataVendor(data_vendor)
    ticker = ticker
    print('Fetching', ticker, 'historical quotes from', dataVendor.getVendorName(), 'database...')
    quotes = dataVendor.fetchQuotes(ticker)
    print(ticker, 'data collected. Adding to database...')
    debugz(con, quotes, dbname, symbol_table_name, price_table_name, dataVendor)
    print(ticker, 'datas inserted.')

ticker = sys.argv[1]
debug(ticker)

