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

    def getLastQuote(self, ticker):
        series = self.db.getLastQuoteDate(ticker, self.symbol_table_name, self.price_table_name)
        timestamp = series[0]
        day, month, year = self.convertTimestampToStrings(timestamp)
        query = Quotemedia().getQuery(ticker, day, month, year)
        print(query)


ticker=sys.argv[1].upper()
utils = Utils()
utils.getLastQuote(ticker)



