from dataVendor import DataVendor

vendor = DataVendor()
quotes = vendor.fetchQuotes(vendor.alphavantage, 'AAPL')
# print(quotes)
