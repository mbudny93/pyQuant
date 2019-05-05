from dataVendor import DataVendor

vendor = DataVendor()
quotes = vendor.fetchQuotes(vendor.tiingo, 'AAPL')
# print(quotes)
