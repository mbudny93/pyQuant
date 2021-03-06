import pandas
import pandas_datareader
import os
import sys

class DataVendor:
    def __init__(self, vendorName):
        self.alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']
        self.tiingo_api_key = os.environ['TIINGO_API_KEY']
        self.vendors = {}

        self.vendors['alphavantage'] = AlphaVantage(self.alphavantage_api_key)
        self.vendors['tiingo'] = Tiingo(self.tiingo_api_key)
        self.vendors['stooq'] = Stooq()
        self.vendors['quotemedia'] = Quotemedia()

        self.vendorName = vendorName

###########################################################################################
    def getVendorName(self):
        return self.vendorName

    def getVendor(self):
        return self.vendors[self.getVendorName()]

    def getQuery(self, ticker):
        return self.getVendor().getQuery(ticker)

############################################################################################

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

    def fetchQuotes(self, ticker):
        fname = self.getVendorName()
        query = self.getQuery(ticker)
        if query:
            return self.fetchFromPandas(query, fname)
        else:
            return self.fetchFromPandasDatareader(ticker, fname)

    def adapt(self, day):
        return self.getVendor().adapt(day)

###########################################################################################

class AlphaVantage:
    def __init__(self, api_key):
        self.alphavantage_api_key = api_key

    def getQuery(self, ticker):
        query = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
        'symbol=%s&outputsize=full&apikey=%s&datatype=csv')%(ticker, self.alphavantage_api_key)
        return query

    def adapt(self, day):
        timestamp, open, high, low, close, volume = day
        return timestamp, open, high, low, close, volume

class Tiingo:
    def __init__(self, api_key):
        self.tiingo_api_key = api_key
        return None

    def getQuery(self, ticker):
        return None

    def adapt(self, day):
        symbol, date, adjClose, adjHigh, adjLow, adjOpen, adjVolume, close, divCash, high, low, open, splitFactor, volume = day
        return date, open, high, low, close, volume

class Stooq:
    def __init__(self):
        return None

    def getQuery(self, ticker):
        query = 'https://stooq.com/q/d/l/?s=%s&i=d'%(ticker)
        return query

    def adapt(self, day):
        # STOCK
        # Date, Open, High, Low, Close, Volume = day
        # return Date, Open, High, Low, Close, Volume

        # FOREX
        Date, Open, High, Low, Close = day
        return Date, Open, High, Low, Close, ''

class Quotemedia:
    def __init__(self):
        return None

    def getQuery(self, ticker):
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
        return query

    def adapt(self, day):
        date, open, high, low, close, volume, changed, changep, adjclose, tradeval, tradevol = day
        return date, open, high, low, close, volume

def writeToCsv(file, quotes):
    f = open(file,"w+")
    f.write(quotes.to_csv())
    f.close()

def readFromCsv(file):
    quotes = pandas.read_csv(file)
    quotes = quotes.dropna()
    print(quotes)

def printColumns(df):
    for col in df.columns:
        print(col)

ticker = 'ftv'
file = "test.csv"
vendorName  = sys.argv[1]

###############################################################TEST
vendor = DataVendor(vendorName)
query = vendor.fetchQuotes(ticker)

# writeToCsv(file, query)
readFromCsv(file)

print('newest data in ohlcv format: ', vendor.adapt(query.values[0]))
print('oldest data in ohlcv format: ', vendor.adapt(query.values[-1]))



