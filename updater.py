from dataVendor import *

class Updater:
    def __init__(self, db_inserter, dataVendor):
        self.db_inserter = db_inserter
        self.dataVendor = dataVendor

    def firstUpdate(self):
        print('There we go...')
        tickerz = self.db_inserter.database.getTickersFromDB()
        for ticker in tickerz:
            print('Fetching', ticker[1], 'historical quotes from', self.dataVendor.getVendorName(), 'database...')
            quotes = self.dataVendor.fetchQuotes(ticker[1])
            print(ticker[1], 'data validated. Adding to database...')
            self.db_inserter.insertQuotes(self.dataVendor, ticker[0], quotes)
            print(ticker[1], 'datas inserted.')
