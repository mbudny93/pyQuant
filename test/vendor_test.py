import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import vendor

def test_quotemedia_vendor_connectivity():
    quotes = vendor.Quotemedia().fetchHistoricalQuotes('aapl')
    assert(not quotes.empty)
    newestQuote = quotes.tail(1)
