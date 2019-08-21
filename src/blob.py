from query import Query

import datetime
import time
import pymysql
import requests
import lxml.html
import sys

class Updater:
    def __init__(self, db_inserter, dataVendor):
        self.db_inserter = db_inserter
        self.dataVendor = dataVendor

    def firstUpdate(self):
        print('There we go...')
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            print('Fetching', ticker[1], 'historical quotes from', self.dataVendor.getVendorName(), 'database...')
            quotes = self.dataVendor.fetchHistoricalQuotes(ticker[1])
            print(ticker[1], 'data validated. Adding to database...')
            self.db_inserter.insertQuotes(self.dataVendor, ticker[0], quotes)
            print(ticker[1], 'datas inserted.')

    def update(self):
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            print('Fetching', ticker[1], 'quotes from', self.dataVendor.getVendorName(), 'database...')
            # quotes = self.dataVendor.fetchHistoricalQuotes(ticker[1])
            # print(ticker[1], 'data validated. Adding to database...')
            # self.db_inserter.insertQuotes(self.dataVendor, ticker[0], quotes)
            print(ticker[1], 'datas inserted.')

class DataInserter:
    def __init__(self, database):
        self.database = database

    def insertSymbols(self):
        with DbSupervisor.connection.cursor() as cursor:
            columns = self.database.getTableColumnNamesFormatted(self.database.symbol_table_name)
            table = self.database.symbol_table_name
            tickers = self.database.getTickersList()
            for symbol in tickers:
                values = symbol[0:-1]
                query = Query.insertSymbols(table, columns, values)
                cursor.execute(query)
                print('Adding', symbol[1], '...')
            print('Database succesfully created.')

    def insertQuotes(self, vendor, ticker_id, quotes):
        with DbSupervisor.connection.cursor() as cursor:
            columns = self.database.getTableColumnNamesFormatted(self.database.price_table_name)
            table = self.database.price_table_name
            preliminary_query = Query.insertQuotes(table, columns)

            for day in quotes.values:
                d, o, h, l, c, v = vendor.adapt(day)
                values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(ticker_id), str(d), str(o), str(h), str(l), str(c), str(v))
                query = preliminary_query + values_query
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                cursor.execute(query)
                # print(query)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            connection.commit()

class DbSupervisor:

    connection = {}

    @staticmethod
    def establishConnection():
        try:
            start = time.time()
            connection = pymysql.connect(host='localhost', user='admin', password='admin')
            end = time.time()
            print('Succesfully connected to local database in', end-start, 'seconds.')
            DbSupervisor.connection = connection
        except:
            DbSupervisor.connection.close()
            sys.exit('FATAL ERROR: Unable to connect to local database.')

    @staticmethod
    def connectToDatabase(dbName):
        try:
            with DbSupervisor.connection.cursor() as cursor:
                start = time.time()
                DbSupervisor.cursor.execute(Query(DbSupervisor.connection).useDatabase(dbName))
                end = time.time()
                print('Successfully connected to database', dbName, 'in', end-start, 'seconds')
        except:
            sys.exit('FATAL ERROR: Unable to connect to database', dbName)

    @staticmethod
    def checkIfDatabaseExists(dbName):
        try:
            with DbSupervisor.connection.cursor() as cursor:
                return cursor.execute(Query.checkIfDatabaseExists(dbName))
        except:
            DbSupervisor.connection.close()
            sys.exit('FATAL ERROR: Unable to perform simple query')

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
        pass

    def fetchHistoricalQuotes(self):
        print('First fetch...')
        time.sleep(3)

    def update(self):
        print('Updating ...')
        time.sleep(3)

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
        url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tickerz = self.__getTickersFromUrl(url)

        self.database.tickers = tickerz
        self.tickers = tickerz

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getTickersFromUrl(self, url):
        print('Generating tickers for us500...')
        html = lxml.html.fromstring(self.__getUrlContent(url))
        tuples = self.__parseHtml(html)
        print('Symbols succesfully generated')
        return tuples

    def __getUrlContent(self, url):
        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')
        return res.content

    def __parseHtml(self, html):
        tickers = html.xpath('//table[1]//td[1]//text()')[0:-1:2]
        securities = html.xpath('//table[1]//td[2]//text()')
        symbols = html.xpath('//table[1]//td[4]//text()')

        now = datetime.datetime.utcnow()

        tuples = []
        for tick, comp, sym in zip(tickers, securities, symbols):
            tup = (tick, comp, sym, now)
            tuples.append(tup)
        return tuples

class Forex(Dataset):
    def generateTickersList(self):
        self.tickers.append('eurusd')

class DataVendor:
    def __init__(self, vendorName):
        self.alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']
        self.tiingo_api_key = os.environ['TIINGO_API_KEY']
        self.vendors = {}

        self.vendors['alphavantage'] = AlphaVantage(self.alphavantage_api_key)
        self.vendors['tiingo'] = Tiingo(self.tiingo_api_key)
        self.vendors['stooq'] = Stooq()
        self.vendors['quotemedia'] = Quotemedia()

        self.vendorName = vendorName

    def getVendorName(self):
        return self.vendorName

    def getVendor(self):
        return self.vendors[self.getVendorName()]

    def getQuery(self, ticker):
        return self.getVendor().getQuery(ticker)

    def getQuery(self, ticker, day, month, year):
        return self.getVendor().getQuery(ticker, day, month, year)

    def fetchFromPandas(self, query, fname):
        try:
            quotes = pandas.read_csv(query)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchFromPandasDatareader(self, ticker, fname):
        try:
            quotes = pandas_datareader.get_data_tiingo(ticker, api_key=self.tiingo_api_key)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchHistoricalQuotes(self, ticker):
        fname = self.getVendorName()
        query = self.getQuery(ticker)
        if query:
            datas = self.fetchFromPandas(query, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)
        else:
            datas = self.fetchFromPandasDatareader(ticker, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)

    def fetchQuotes(self, ticker, day, month, year):
        fname = self.getVendorName()
        query = self.getQuery(ticker, day, month, year)
        if query:
            datas = self.fetchFromPandas(query, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)
        else:
            datas = self.fetchFromPandasDatareader(ticker, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)

    def adapt(self, day):
        return self.getVendor().adapt(day)

    def validateDataset(self, datas):
        return self.getVendor().validateDataset(datas)

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

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

class Tiingo:
    def __init__(self, api_key):
        self.tiingo_api_key = api_key
        return None

    def getQuery(self, ticker):
        return None

    def adapt(self, day):
        symbol, date, adjClose, adjHigh, adjLow, adjOpen, adjVolume, close, divCash, high, low, open, splitFactor, volume = day
        return date, open, high, low, close, volume

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

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

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

class Quotemedia:
    def __init__(self):
        return None

    def getQuery(self, ticker):
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
        return query

    def getQuery(self, ticker, day, month, year):
        # query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            # '&startDay=%s&startMonth=%s&startYear=%s&endDay=20&endMonth=5&endYear=2019&isRanged=true&symbol=%s')%(day, month, year, ticker)
        ####################TESTXXX
        month -= 1
        if month < 1 :
            month = 12
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=%s&startMonth=%s&startYear=%s&isRanged=true&symbol=%s')%(day, month, year, ticker)
        return query

    def adapt(self, day):
        date, open, high, low, close, volume, changed, changep, adjclose, tradeval, tradevol = day
        return date, open, high, low, close, volume

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas
