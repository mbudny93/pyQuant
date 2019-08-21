from query import Query
from vendor import *
from database import Database
from supervisor import *

import datetime
import time
import requests
import lxml.html
import sys

# abstraction layer over database
class Dataset:

    name = ''
    database = None
    updater = None
    tickers = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CREATE
    def __init__(self, name):
        print('Initializing new dataset ...')
        self.name = name
        self.database = Database(self.name)
        self.database.createDatabase()
        self.database.createTables()

        self.generateTickersList()
        self.database.setVendor(self.createVendor())

        self.database.insertSymbols()
        print("Dataset succesfully created.")


    def fill(self):
        self.database.firstUpdate()

    def update(self):
        print('Updating ...')
        time.sleep(3)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove(self):
        self.database.dropDatabase()

    def getInfo(self):
        pass

    def createVendor(self):
        raise NotImplementedError()

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

    def createVendor(self):
        return Quotemedia()

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
