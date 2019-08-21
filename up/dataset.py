from dbSupervisor import DbSupervisor
from query import Query

import datetime
import time
import pymysql
import requests
import lxml.html
import sys

class Database:

    db_name = ''
    symbol_table_name = ''
    price_table_name = ''
    tickers = []

    def __init__(self, db_name):
        self.db_name = db_name
        self.symbol_table_name = 'symbol'
        self.price_table_name = 'daily_price'

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

# abstraction layer over database
class Dataset:

    name = ''
    database = {}
    tickers = []

    def __init__(self, name):
        print('Initializing new dataset ...')
        self.name = name
        self.database = Database(self.name)
        self.database.createDatabase()
        self.database.createTables()
        self.generateTickersList()
        self.database.insertSymbols()
        print("Dataset succesfully created.")

    def create(self):
        self.database = Database(self.name)
        self.database.createDatabase()

    def update(self):
        pass

    def remove(self):
        self.database.dropDatabase()

    def getInfo(self):
        pass

    def generateTickersList(self):
        raise NotImplementedError()

    def getTickersList(self):
        pass

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        pass

class US500(Dataset):
    def generateTickersList(self):
        print('Generating tickers for us500...')
        now = datetime.datetime.utcnow()
        url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[1]//td[1]//text()')[0:-1:2]
        securities = html.xpath('//table[1]//td[2]//text()')
        symbols = html.xpath('//table[1]//td[4]//text()')

        tuples = []
        for tick, comp, sym in zip(tickers, securities, symbols):
            tup = (tick, comp, sym, now)
            tuples.append(tup)
        print('Symbols succesfully generated')

        self.database.tickers = tuples
        self.tickers = tuples

class Forex(Dataset):
    def generateTickersList(self):
        self.tickers.append('eurusd')
