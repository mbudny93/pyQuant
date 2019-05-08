from dataVendor import *

class Updater:
    def __init__(self, db_inserter, dataVendor):
        self.db_inserter = db_inserter
        self.dataVendor = dataVendor

    def firstUpdate(self):
        print('There we go...')
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            print('Fetching', ticker, 'historical quotes from', self.dataVendor.getVendorName(), 'database...')
            quotes = self.dataVendor.fetchQuotes(ticker)
            print(ticker, 'data validated. Adding to database...')
            self.db_inserter.insertQuotes(self.dataVendor, quotes)
            print(ticker, 'datas inserted.')
