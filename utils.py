from database import Database
from query import Query
from barchart import Chart
from dataVendor import DataVendor, Quotemedia

import pymysql
import sys

class Utils:
    def __init__(self):
        return None
    def convertTimestampToStrings(self, timestamp):
        return timestamp.day, timestamp.month, timestamp.year


ticker=sys.argv[1].upper()
connection = pymysql.connect(host='localhost', user='admin', password='admin')
##############################################################################
dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'
##############################################################################
db = Database(connection, dbname)
db.connectToDatabase()
series = db.getLastQuoteDate(ticker, symbol_table_name, price_table_name)
timestamp = series[0]
day, month, year = Utils().convertTimestampToStrings(timestamp)
query = Quotemedia().getQuery(ticker, day, month, year)
print(query)


