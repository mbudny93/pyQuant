from database import Database
from query import Query
from barchart import Chart
from dataVendor import DataVendor, Quotemedia

import pymysql
import sys

class Utils:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='admin', password='admin')
        self.dbname = 'test'
        self.symbol_table_name = 'symbol'
        self.price_table_name = 'daily_price'
        self.db = Database(self.connection, self.dbname)
        self.db.connectToDatabase()

    def convertTimestampToStrings(self, timestamp):
        return timestamp.day, timestamp.month, timestamp.year

    def getQuotesFromVendor(self):
        pass

    def getQuotesFromDB(self):
        pass

    def getLastQuoteFromDB(self, ticker, order = 'DESC'):
        series = self.db.getLastQuoteDate(ticker, self.symbol_table_name, self.price_table_name, order)
        timestamp = series[0]
        day, month, year = self.convertTimestampToStrings(timestamp)
        query = Quotemedia().getQuery(ticker, day, month, year)
        print(query)
        vendor = DataVendor('quotemedia')
        quotes = vendor.fetchQuotes(ticker, day, month, year)
        print(quotes)


default_ticker = 'AAPL'
if len(sys.argv) is 1:
    ticker = default_ticker
else:
    ticker=sys.argv[1].upper()

utils = Utils()
utils.getLastQuoteFromDB(ticker)



