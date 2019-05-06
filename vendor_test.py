from dataVendor import DataVendor
import pandas

def writeToCsv(file, ticker, v, vendor):
    quotes = v.fetchQuotes(vendor, ticker)
    f = open(file,"w+")
    f.write(quotes.to_csv())
    f.close()

def readFromCsv(file):
    quotes = pandas.read_csv(file)
    print(quotes)

def testCsv(file):
    quotes = pandas.read_csv(file)
    print(str(quotes.head()))

v = DataVendor()
file = 'test.csv'
ticker = 'aapl.us'
vendor = v.stooq

writeToCsv(file, ticker, v, vendor)
# readFromCsv(file)
testCsv(file)

