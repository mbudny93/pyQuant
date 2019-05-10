from database import Database
from query import Query
from barchart import *
import pymysql
import pandas.io.sql as psql

connection = pymysql.connect(host='localhost', user='admin', password='admin')
##############################################################################
dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'
vendorName = 'quotemedia'
ticker = 'AAPL'
##############################################################################
db = Database(connection, dbname)
db.connectToDatabase()
quotes = db.getQuotes(ticker, symbol_table_name, price_table_name)
# plot(quotes)
# print(quotes)





