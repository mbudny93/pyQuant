import pandas

class DataVendor:

    def __init__(self):
        pass

    def getVendorName(self):
        return self.vendorName

    def getQuery(self, ticker):
        raise NotImplementedError()

    def adapt(self, day):
        raise NotImplementedError()

    def validateDataset(self, datas):
        datas = datas.dropna()
        return datas

    def fetchFromPandas(self, query, fname):
        try:
            quotes = pandas.read_csv(query)
            return quotes
        except:
            sys.exit('FATAL ERROR: Connection with', fname, 'failed')

class Quotemedia(DataVendor):

    def __init__(self):
        self.vendorName = 'Quotemedia'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fetchHistoricalQuotes(self, ticker):
        fname = self.getVendorName()
        query = self.getQuery(ticker)
        datas = self.fetchFromPandas(query, fname)
        print(ticker, 'data collected. Validating dataset...')
        return self.validateDataset(datas)

    def fetchQuotes(self, ticker, day, month, year):
        fname = self.getVendorName()
        query = self.getQuery(ticker, day, month, year)
        datas = self.fetchFromPandas(query, fname)
        print(ticker, 'data collected. Validating dataset...')
        return self.validateDataset(datas)

    def getQuery(self, ticker):
        query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
        return query

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def adapt(self, day):
        date, open, high, low, close, volume, changed, changep, adjclose, tradeval, tradevol = day
        return date, open, high, low, close, volume

    # def getQuery(self, ticker, day, month, year):
        # # query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            # # '&startDay=%s&startMonth=%s&startYear=%s&endDay=20&endMonth=5&endYear=2019&isRanged=true&symbol=%s')%(day, month, year, ticker)
        # ####################TESTXXX
        # month -= 1
        # if month < 1 :
            # month = 12
        # query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
            # '&startDay=%s&startMonth=%s&startYear=%s&isRanged=true&symbol=%s')%(day, month, year, ticker)
        # return query

# q = Quotemedia()
# print(q.getVendorName())
