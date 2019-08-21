from database import DbConnectionWrapper
from query import Query

import datetime
import time
import pymysql
import pandas.io.sql as psql
import requests
import lxml.html
import sys

# abstraction layer over database
class Dataset:
    def __init__(self, name):
        self.name = name
        # print(__class__.__name__)
        database = Database(name)
        database.dropDatabase()
        database.createDatabase()
        database.createTables()
        database.generateTickersList()
        database.getTickersList()

        self.tickers = []

    def prepareDataset(self):
        self.generateTickerList()
        database = Database


    def createDatabase(self):
        self.database = Database(self.name)
        self.database.createDatabase()
        pass

    def dropDatabase(self):
        pass

    def init(self):
        pass

    def update(self):
        print('update')

    def generateTickersList(self):
        raise NotImplementedError()

    def getTickersList(self):
        pass

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        pass

class US500(Dataset):
    def generateTickersList(self):
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

class Forex(Dataset):
    def generateTickersList(self):
        self.tickers.append('eurusd')


DbConnectionWrapper.establishConnection()
# DbConnectionWrapper.connectToDatabase('test')

datasets = []
datasets.append(US500('us500'))
datasets.append(Forex('forex'))

for ds in datasets:
    ds.init()


DbConnectionWrapper
    establishConnection()
    connectToDatabase()

DbSupervisor
    getDatabaseInfo()

Dataset
    create()
        database.drop()
        database.create()
        database.connect()
        dataset.generateTickerList()
        database.fillTickers()
        database.fill()

    update()
        database.connect()
        database.update()

    remove()
        database.drop()

    getInfo()
        database.print()

