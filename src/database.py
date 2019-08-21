from query import Query
from vendor import *
from supervisor import *

import time
import sys

class Database:

    db_name = ''
    symbol_table_name = ''
    price_table_name = ''
    tickers = []
    dataVendor = None

    def __init__(self, db_name):
        self.db_name = db_name
        self.symbol_table_name = 'symbol'
        self.price_table_name = 'daily_price'

    def setVendor(self, vendor):
        self.dataVendor = vendor

    def createDatabase(self):
        with DbSupervisor.connection.cursor() as cursor:
            try:
                if DbSupervisor.checkIfDatabaseExists(self.db_name):
                    self.dropDatabase()
                cursor.execute(Query.createDatabase(self.db_name))
                # use database
                cursor.execute(Query.useDatabase(self.db_name))
                print('Database', self.db_name, 'succesfully created')
            except:
                sys.exit('FATAL ERROR: Unable to create database', dbName)

    def dropDatabase(self):
        with DbSupervisor.connection.cursor() as cursor:
            try:
                cursor.execute(Query.dropDatabase(self.db_name))
                print('Database', self.db_name, 'succesfully deleted')
            except:
                sys.exit('FATAL ERROR: Unable to remove database', dbName)

    def createTables(self):
        create_symbol_table_query, create_price_table_query = Query.createTables(self.symbol_table_name, self.price_table_name)
        with DbSupervisor.connection.cursor() as cursor:
            try:
                cursor.execute(create_symbol_table_query)
                cursor.execute(create_price_table_query)
                DbSupervisor.connection.commit()
                print('Tables', self.symbol_table_name, 'and' , self.price_table_name, 'succesfully created')
            except:
                sys.exit('FATAL ERROR: Unable to create tables', dbName)

    def insertSymbols(self):
        with DbSupervisor.connection.cursor() as cursor:
            columns = self.getTableColumnNamesFormatted(self.symbol_table_name)
            table = self.symbol_table_name
            tickers = self.getTickersList()
            for symbol in tickers:
                values = symbol[0:-1]
                query = Query.insertSymbols(table, columns, values)
                cursor.execute(query)
                print('Adding', symbol[1], '...')
            print('Database symbols succesfully inserted.')

    def getTickersList(self):
        return self.tickers

    def getTickersFromDB(self):
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute(Query.getTickers(self.symbol_table_name))
            result = cursor.fetchall()

            tickerz = []
            for tck in result:
                tickerz.append(tck)
            return tickerz

    def getTableColumnNames(self, table_name):
        with DbSupervisor.connection.cursor() as cursor:
            try:
                cursor.execute(Query.getTableColumnNames(self.db_name, table_name))
                result = cursor.fetchall()
                return result
            except:
                sys.exit('FATAL ERROR: Unable to fetch table column names')

    def getTableColumnNamesFormatted(self, table_name):
        result = self.getTableColumnNames(table_name)
        result = result[1:]

        columns = ''
        for idx, column in enumerate(result):
            columns+=column[0]
            columns+=", "
        columns = columns[0:-2]
        return columns

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        start = time.time()
        query = Query(self.connection).getQuotes(ticker, symbol_table_name, price_table_name)
        # print(query)
        result = psql.read_sql(query, con=self.connection)
        end = time. time()
        print("Fetching from DB completed in", end-start, "seconds")
        return result

    def getLastQuote(self, ticker, symbol_table_name, price_table_name):
        start = time.time()
        query = Query(self.connection).getLastQuote(ticker, symbol_table_name, price_table_name)
        # print(query)
        result = psql.read_sql(query, con=self.connection)
        end = time. time()
        print("Fetching from DB completed in", end-start, "seconds")
        return result

    def getLastQuoteDate(self, ticker, symbol_table_name, price_table_name, order):
        start = time.time()
        query = Query(self.connection).getLastQuote(ticker, symbol_table_name, price_table_name, order)
        # print(query)
        result = psql.read_sql(query, con=self.connection)
        end = time. time()
        print("Fetching from DB completed in", end-start, "seconds")
        return result['price_date']

    def insertQuotes(self, vendor, ticker_id, quotes):
        with DbSupervisor.connection.cursor() as cursor:
            columns = self.getTableColumnNamesFormatted(self.price_table_name)
            table = self.price_table_name
            preliminary_query = Query.insertQuotes(table, columns)

            for day in quotes.values:
                d, o, h, l, c, v = vendor.adapt(day)
                values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(ticker_id), str(d), str(o), str(h), str(l), str(c), str(v))
                query = preliminary_query + values_query
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                cursor.execute(query)
                # print(query)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            DbSupervisor.connection.commit()

    def firstUpdate(self):
        print('There we go...')
        tickerz = self.getTickersFromDB()
        # print(tickerz)
        for ticker in tickerz:
            print('Fetching', ticker[1], 'historical quotes from', self.dataVendor.getVendorName(), 'database...')
            quotes = self.dataVendor.fetchHistoricalQuotes(ticker[1])
            print(ticker[1], 'data validated. Adding to database...')
            self.insertQuotes(self.dataVendor, ticker[0], quotes)
            print(ticker[1], 'datas inserted.')

    def update(self):
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            print('Fetching', ticker[1], 'quotes from', self.dataVendor.getVendorName(), 'database...')
            # quotes = self.dataVendor.fetchHistoricalQuotes(ticker[1])
            # print(ticker[1], 'data validated. Adding to database...')
            # self.db_inserter.insertQuotes(self.dataVendor, ticker[0], quotes)
            print(ticker[1], 'datas inserted.')
