import pymysql
import requests
import datetime
import lxml.html
import time
import pandas
import pandas_datareader
import os

class Database:
    def __init__(self, connection, db_name):
        self.connection = connection
        self.cursor = connection.cursor()
        self.db_name = db_name
        # remove if exists
        self.dropDatabase()
        # create database
        self.cursor.execute(Query(self.connection).createDatabase(db_name))
        # use database
        self.cursor.execute(Query(self.connection).useDatabase(db_name))
        print('Database', self.db_name, 'succesfully created')

    def dropDatabase(self):
        query = Query(self.connection).dropDatabase(self.db_name)
        try:
            self.cursor.execute(query)
            print('Database', self.db_name, 'succesfully deleted')
        except:
            pass

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
        for idx, tck in enumerate(result):
            tickerz.append(tck[0])
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

class Query:
    def __init__(self, connection):
        self.connection = connection

    def createDatabase(self, dbname):
        query = 'create database %s;'%(dbname)
        return query

    def useDatabase(self, dbname):
        query = 'use %s;'%(dbname)
        return query

    def dropDatabase(self, dbname):
        query = 'drop database %s;'%(dbname)
        return query

    def createTables(self, symbol_table_name, price_table_name):
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

    def getTableColumnNames(self, db_name, table_name):
        query = ('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE'
            '`TABLE_SCHEMA`=\'%s\' AND `TABLE_NAME`=\'%s\';')%(db_name, table_name)
        return query

    def insertSymbols(self, symbol_table_name, columns, values):
        query = 'INSERT INTO %s (%s) VALUES %s'%(symbol_table_name, columns, values)
        return query

    def getTickers(self, symbol_table_name):
        query = 'SELECT ticker FROM %s'%(symbol_table_name)
        return query

    def insertQuotes(self, price_table_name, columns):
        query = 'INSERT INTO %s (%s) VALUES '%(price_table_name, columns)
        return query

class DataInserter:
    def __init__(self, database):
        self.database = database
    def insertSymbols(self):
        connection = self.database.connection
        cursor = connection.cursor()
        columns = self.database.getTableColumnNamesFormatted(self.database.symbol_table_name)
        table = self.database.symbol_table_name
        tickers = self.database.getTickersList()
        for symbol in tickers:
            values = symbol[0:-1]
            query = Query(connection).insertSymbols(table, columns, values)
            cursor.execute(query)
            print('Adding', symbol[1], '...')
        print('Database succesfully created.')

    def insertQuotes(self, vendor, quotes):
        connection = self.database.connection
        cursor = connection.cursor()
        columns = self.database.getTableColumnNamesFormatted(self.database.price_table_name)
        table = self.database.price_table_name
        preliminary_query = Query(connection).insertQuotes(table, columns)

        for day in quotes.values:
            d, o, h, l, c, v = vendor.adapt(day)
            values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(d), str(o), str(h), str(l), str(c), str(v))
            query = preliminary_query + values_query
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            cursor.execute(query)
            # print(query)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        connection.commit()


class DataVendor:
    def __init__(self, vendorName):
        #self.alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']
        self.alphavantage_api_key = "null"
        #self.tiingo_api_key = os.environ['TIINGO_API_KEY']
        self.tiingo_api_key = "null"
        self.vendors = {}

        self.vendors['alphavantage'] = AlphaVantage(self.alphavantage_api_key)
        self.vendors['tiingo'] = Tiingo(self.tiingo_api_key)
        self.vendors['stooq'] = Stooq()
        self.vendors['quotemedia'] = Quotemedia()

        self.vendorName = vendorName

###########################################################################################
    def getVendorName(self):
        return self.vendorName

    def getVendor(self):
        return self.vendors[self.getVendorName()]

    def getQuery(self, ticker):
        return self.getVendor().getQuery(ticker)

############################################################################################

    def fetchFromPandas(self, query, fname):
        try:
            quotes = pandas.read_csv(query)
            # print('Data successfully fetched from', fname)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchFromPandasDatareader(self, ticker, fname):
        try:
            quotes = pandas_datareader.get_data_tiingo(ticker, api_key=self.tiingo_api_key)
            # print('Data successfully fetched from', fname)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchQuotes(self, ticker):
        fname = self.getVendorName()
        query = self.getQuery(ticker)
        if query:
            return self.fetchFromPandas(query, fname)
        else:
            return self.fetchFromPandasDatareader(ticker, fname)

    def adapt(self, day):
        return self.getVendor().adapt(day)

###########################################################################################

class AlphaVantage:
    def __init__(self, api_key):
        self.alphavantage_api_key = api_key

    def getQuery(self, ticker):
        query = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
        'symbol=%s&outputsize=full&apikey=%s&datatype=csv')%(ticker, self.alphavantage_api_key)
        return query

    def adapt(self, day):
        timestamp, open, high, low, close, volume = day
        return timestamp, open, high, low, close, volume

class Tiingo:
    def __init__(self, api_key):
        self.tiingo_api_key = api_key
        return None

    def getQuery(self, ticker):
        return None

    def adapt(self, day):
        symbol, date, adjClose, adjHigh, adjLow, adjOpen, adjVolume, close, divCash, high, low, open, splitFactor, volume = day
        return date, open, high, low, close, volume

class Stooq:
    def __init__(self):
        return None

    def getQuery(self, ticker):
        query = 'https://stooq.com/q/d/l/?s=%s&i=d'%(ticker)
        return query

    def adapt(self, day):
        # STOCK
        # Date, Open, High, Low, Close, Volume = day
        # return Date, Open, High, Low, Close, Volume

        # FOREX
        Date, Open, High, Low, Close = day
        return Date, Open, High, Low, Close, ''

class Quotemedia:
    def __init__(self):
        return None

    def getQuery(self, ticker):
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
        return query

    def adapt(self, day):
        date, open, high, low, close, volume, changed, changep, adjclose, tradeval, tradevol = day
        return date, open, high, low, close, volume

class Updater:
    def __init__(self, db_inserter, dataVendor):
        self.db_inserter = db_inserter
        self.vendor = dataVendor

    def firstUpdate(self):
        print('There we go...')
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('Fetching', ticker, 'historical quotes from', dataVendor.getVendorName(), 'database...')
            quotes = dataVendor.fetchQuotes(ticker)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # VALIDATE QUOTES BEFORE INSERTING TO DATABASE
            print(ticker, 'data collected. Validating dataset...')
            quotes = quotes.dropna()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print(ticker, 'data validated. Adding to database...')
            self.db_inserter.insertQuotes(self.vendor, quotes)
            print(ticker, 'datas inserted.')
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##############################################################################
vendorName = 'quotemedia'
dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'
connection = pymysql.connect(host='localhost', user='admin', password='admin')
##############################################################################
db = Database(connection, dbname)
db.createTables(symbol_table_name, price_table_name)
db.createTickersList()
dbInserter = DataInserter(db)
dbInserter.insertSymbols()
##############################################################################
dataVendor = DataVendor(vendorName)
updater = Updater(dbInserter, dataVendor)
##############################################################################
##############################################################################
updater.firstUpdate()
##############################################################################
##############################################################################

