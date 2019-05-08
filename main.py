from database import Database
from dataInserter import DataInserter
from dataVendor import *
from updater import Updater

import pymysql

connection = pymysql.connect(host='localhost', user='admin', password='admin')
##############################################################################
dbname = 'test'
symbol_table_name = 'symbol'
price_table_name = 'daily_price'
vendorName = 'quotemedia'
##############################################################################
db = Database(connection, dbname)
db.createTables(symbol_table_name, price_table_name)
db.createTickersList()
##############################################################################
dbInserter = DataInserter(db)
dbInserter.insertSymbols()
##############################################################################
dataVendor = DataVendor(vendorName)
updater = Updater(dbInserter, dataVendor)
##############################################################################
updater.firstUpdate()
##############################################################################
