from database import Database
from query import Query
from barchart import Chart

import pymysql
import sys

ticker=sys.argv[1].upper()
connection = pymysql.connect(host='localhost', user='admin', password='admin')
##############################################################################
dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'
##############################################################################
db = Database(connection, dbname)
db.connectToDatabase()
quotes = db.getQuotes(ticker, symbol_table_name, price_table_name)
chart = Chart()
chart.plox(quotes)





