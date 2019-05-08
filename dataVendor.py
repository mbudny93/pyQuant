import pandas
import pandas_datareader
import os

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

    def getVendorName(self):
        return self.vendorName

    def getVendor(self):
        return self.vendors[self.getVendorName()]

    def getQuery(self, ticker):
        return self.getVendor().getQuery(ticker)

    def fetchFromPandas(self, query, fname):
        try:
            quotes = pandas.read_csv(query)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchFromPandasDatareader(self, ticker, fname):
        try:
            quotes = pandas_datareader.get_data_tiingo(ticker, api_key=self.tiingo_api_key)
            return quotes
        except:
            print('Connection with', fname, 'failed.')
            return[]

    def fetchQuotes(self, ticker):
        fname = self.getVendorName()
        query = self.getQuery(ticker)
        if query:
            datas = self.fetchFromPandas(query, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)
        else:
            datas = self.fetchFromPandasDatareader(ticker, fname)
            print(ticker, 'data collected. Validating dataset...')
            return self.validateDataset(datas)

    def adapt(self, day):
        return self.getVendor().adapt(day)

    def validateDataset(self, datas):
        return self.getVendor().validateDataset(datas)

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

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

class Tiingo:
    def __init__(self, api_key):
        self.tiingo_api_key = api_key
        return None

    def getQuery(self, ticker):
        return None

    def adapt(self, day):
        symbol, date, adjClose, adjHigh, adjLow, adjOpen, adjVolume, close, divCash, high, low, open, splitFactor, volume = day
        return date, open, high, low, close, volume

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

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

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

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

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas
