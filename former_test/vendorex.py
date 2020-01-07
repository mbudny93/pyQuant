import pandas


def getQuery(ticker):
    query = ('http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501'
        '&startDay=1&startMonth=1&startYear=2010&&symbol=%s')%(ticker)
    return query

def fetchFromPandas(query):
    try:
        quotes = pandas.read_csv(query)
        return quotes
    except:
        sys.exit('FATAL ERROR: Connection with dupa failed')

tck = 'aapl'
res = fetchFromPandas(getQuery(tck))
print(res)
