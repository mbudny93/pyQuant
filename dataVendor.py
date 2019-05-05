import pandas
import pandas_datareader as pdr
import os

class DataVendor:
    def _init_(self):
        alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']
        tiingo_api_key = os.environ['TIINGO_API_KEY']

    def fetchQuotesFromVendor(self, ticker):
        return True

    def fetchQuotesFrom_alphavantage(self, ticker):
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&\
        symbol=%s&outputsize=full&apikey=%s&datatype=csv'%(ticker, alphavantage_api_key)
        try:
            quotes = pandas.read_csv(query)
            return quotes
        except:
            print('Connection to alphavantage failed.')
            return[]

    def fetchQuotesFrom_tiingo(self, ticker):
        query = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&\
        symbol=%s&outputsize=full&apikey=%s&datatype=csv'%(ticker, tiingo_api_key)
        try:
            quotes = pdr.get_data_tiingo(ticker, tiingo_api_key)
            return quotes
        except:
            print('Connection to tiingo failed.')
            return[]

    def fetchQuotesFrom_stooq(self, ticker):
        query = 'https://stooq.com/q/d/l/?s=%s&i=d'%(ticker)
        try:
            quotes = pandas.read_csv(query)
            return quotes
        except:
            print('Connection to stooq failed.')
            return[]

