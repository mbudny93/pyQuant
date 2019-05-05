import pandas
import pandas_datareader
import os

class DataVendor:

    def __init__(self):
        self.alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']
        self.tiingo_api_key = os.environ['TIINGO_API_KEY']

###########################################################################################

    def fetchQuotes(self, vendor, *ticker):
        fname = vendor.__name__
        query = vendor(*ticker)
        if query:
            return self.fetchFromPandas(query, fname)
        else:
            return self.fetchFromPandasDatareader(*ticker, fname)

    def fetchFromPandas(self, query, fname):
        try:
            quotes = pandas.read_csv(query)
            print('Data successfully fetched from', fname)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchFromPandasDatareader(self, ticker, fname):
        try:
            quotes = pandas_datareader.get_data_tiingo(ticker, api_key=self.tiingo_api_key)
            print('Data successfully fetched from', fname)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

###########################################################################################

    def alphavantage(self, ticker):
        query = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
        'symbol=%s&outputsize=full&apikey=%s&datatype=csv')%(ticker, self.alphavantage_api_key)
        return query

    def tiingo(self, ticker):
        return None

    def stooq(self, ticker):
        query = 'https://stooq.com/q/d/l/?s=%s&i=d'%(ticker)
        return query

    def quotemedia(self, ticker):
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
        return query
