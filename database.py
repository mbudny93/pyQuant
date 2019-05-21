from query import Query

import datetime
import time
import pymysql
import pandas.io.sql as psql
import requests
import lxml.html

class Database:
    def __init__(self, connection, db_name):
        self.connection = connection
        self.cursor = connection.cursor()
        self.db_name = db_name

    def createDatabase(self):
        # create database
        self.cursor.execute(Query(self.connection).createDatabase(self.db_name))
        # use database
        self.cursor.execute(Query(self.connection).useDatabase(self.db_name))
        print('Database', self.db_name, 'succesfully created')

    def dropDatabase(self):
        # remove if exists
        query = Query(self.connection).dropDatabase(self.db_name)
        try:
            self.cursor.execute(query)
            print('Database', self.db_name, 'succesfully deleted')
        except:
            pass

    def connectToDatabase(self):
        self.cursor.execute(Query(self.connection).useDatabase(self.db_name))
        print('Successfully connected to database:', self.db_name)

    def createTables(self, symbol_table_name, price_table_name):
        self.symbol_table_name = symbol_table_name
        self.price_table_name = price_table_name
        self.symbol_table, self.price_table = Query(self.connection).createTables(symbol_table_name, price_table_name)
        try:
            self.cursor.execute(self.symbol_table)
            self.cursor.execute(self.price_table)
            self.connection.commit()
            print('Tables', symbol_table_name, 'and' ,price_table_name, 'succesfully created')
        finally:
            pass

    def createTickersList(self):
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

        self.tickers = tuples

    def getTickersList(self):
        return self.tickers

    def getTickersFromDB(self):
        self.cursor.execute(Query(self.connection).getTickers(self.symbol_table_name))
        result = self.cursor.fetchall()

        tickerz = []
        for tck in result:
            tickerz.append(tck)
        return tickerz

    def getTableColumnNames(self, table_name):
        try:
            self.cursor.execute(Query(self.connection).getTableColumnNames(self.db_name, table_name))
            result = self.cursor.fetchall()
            return result
        finally:
            pass

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

    def getLastQuoteDate(self, ticker, symbol_table_name, price_table_name):
        start = time.time()
        query = Query(self.connection).getLastQuote(ticker, symbol_table_name, price_table_name)
        # print(query)
        result = psql.read_sql(query, con=self.connection)
        end = time. time()
        print("Fetching from DB completed in", end-start, "seconds")
        return result['price_date']



