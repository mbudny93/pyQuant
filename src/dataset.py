from query import Query
from vendor import *
from database import Database
from supervisor import *
from scrap import *

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

    def __init__(self, name):
        self.name = name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create(self):
        print('Initializing new dataset ...')

        self.database = Database(self.name)
        self.database.createDatabase()
        self.database.createTables()

        self.generateTickersList()
        self.database.insertSymbols()
        self.database.setVendor(self.createVendor())

        print("Dataset succesfully created.")

    def fill(self):
        DbSupervisor.connectToDatabase(self.name)
        print('First fetch...')
        time.sleep(2)
        # self.database.firstUpdate()

    def update(self):
        DbSupervisor.connectToDatabase(self.name)
        print('Updating ...')
        time.sleep(2)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def use(self):
        if DbSupervisor.databaseExists(self.getName()):
            print(self.getName(), 'dataset exists. What to do?')
        else:
            print(self.getName(), 'Initializing dataset ', self.getName(), ' ...')

    def remove(self):
        self.database.dropDatabase()

    def getInfo(self):
        pass

    def getName(self):
        return self.name

    def createVendor(self):
        raise NotImplementedError()

    def generateTickersList(self):
        raise NotImplementedError()

    def getTickersList(self):
        pass

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class US500(Dataset):
    def generateTickersList(self):
        tickerz = scrap_us500()
        self.tickers = self.database.tickers = tickerz

    def createVendor(self):
        return Quotemedia()

class DAX30(Dataset):
    def generateTickersList(self):
        tickerz = scrap_dax()
        self.tickers = self.database.tickers = tickerz

    def createVendor(self):
        return Quotemedia()

class FTSE100(Dataset):
    def generateTickersList(self):
        tickerz = scrap_ftse100()
        self.tickers = self.database.tickers = tickerz

    def createVendor(self):
        return Quotemedia()

class WIG20(Dataset):
    def generateTickersList(self):
        tickerz = scrap_wig20()
        self.tickers = self.database.tickers = tickerz

    def createVendor(self):
        return Quotemedia()
