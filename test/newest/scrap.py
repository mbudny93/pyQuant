import requests
import lxml.html
import sys

url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
url2 = 'https://en.wikipedia.org/wiki/DAX'

try:
    res = requests.get(url2)
except:
    sys.exit('FATAL ERROR: Unable to connect to url ...')

html = lxml.html.fromstring(res.content)

# print(dir(html))
# print(html.text)

tickers = html.xpath('//table[3]//td[2]//text()')#[0:-1:2]
# print(tickers)
securities = html.xpath('//table[3]//td[3]//text()')
# print(securities)
symbols = html.xpath('//table[3]//td[4]//text()')
# print(symbols)

tuples = []
for tick, comp, sym in zip(tickers, securities, symbols):
    tup = (tick, comp, sym)
    tuples.append(tup)

print(tuples)
