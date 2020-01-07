from src import vendor

def test_quotemedia_vendor_connectivity():
    quotes = vendor.Quotemedia().fetchHistoricalQuotes('aapl')
    print(quotes)
    #print(type(quotes))
