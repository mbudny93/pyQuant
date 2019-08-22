import sys
import requests
import lxml.html


def scrap_djia():
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        ticker = html.xpath('//table[2]//td[3]//text()')[0:-1:2]
        security = html.xpath('//table[2]//td[1]//text()')[0:-1:2]
        sector = html.xpath('//table[2]//td[4]//text()')[0:-1:2]

        tuples = []
        for tick, comp, sec in zip(ticker, security, sector):
            tup = (tick, comp, sec)
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_nasdaq100():
        url = 'https://en.wikipedia.org/wiki/NASDAQ-100'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        ticker = html.xpath('//table[3]//td[2]//text()')
        security = html.xpath('//table[3]//td[1]//text()')

        tuples = []
        for tick, comp in zip(ticker, security):
            tup = (tick[:-1], comp, 'NASDAQ Composite')
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_us500():
        url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        ticker = html.xpath('//table[1]//td[1]//text()')[0:-1:2]
        security = html.xpath('//table[1]//td[2]//text()')
        sector = html.xpath('//table[1]//td[4]//text()')

        tuples = []
        for tick, comp, sec in zip(ticker, security, sector):
            tup = (tick, comp, sec)
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_dax():
        url = 'https://en.wikipedia.org/wiki/DAX'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[3]//td[4]//text()')
        security = html.xpath('//table[3]//td[2]//text()')
        sector = html.xpath('//table[3]//td[3]//text()')

        tuples = []
        for tick, comp, sec in zip(tickers, security, sector):
            tup = (tick, comp, sec)
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_ftse100():
        url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[3]//td[2]//text()')
        security = html.xpath('//table[3]//td[1]//text()')
        sector = html.xpath('//table[3]//td[3]//text()')

        tuples = []
        for tick, comp, sec in zip(tickers, security, sector):
            tup = (tick, comp, sec[:-1])
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_cac40():
        url = 'https://en.wikipedia.org/wiki/CAC_40'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[3]//td[3]//text()')
        security = html.xpath('//table[3]//td[1]//text()')
        sector = html.xpath('//table[3]//td[2]//text()')

        tuples = []
        for tick, comp, sec in zip(tickers, security, sector):
            tup = (tick[4:-1], comp, sec)
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

#incorrect
def scrap_smi():
        url = 'https://en.wikipedia.org/wiki/Swiss_Market_Index'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[2]//td[4]//text()')
        security = html.xpath('//table[2]//td[1]//text()')
        sector = html.xpath('//table[2]//td[2]//text()')

        tuples = []
        for tick, comp, sec in zip(tickers, security, sector):
            tup = (tick, comp, sec)
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

def scrap_wig20():
        url = 'https://pl.wikipedia.org/wiki/WIG20'

        try:
            res = requests.get(url)
        except:
            sys.exit('FATAL ERROR: Unable to connect to url ...')

        html = lxml.html.fromstring(res.content)

        tickers = html.xpath('//table[1]//td[2]//text()')
        security = html.xpath('//table[1]//td[1]//text()')[0:-1:2]
        sector = html.xpath('//table[1]//td[3]//text()')

        tuples = []
        for tick, comp, sec in zip(tickers, security, sector):
            tup = (tick.rstrip(), comp.rstrip(), sec.rstrip())
            tuples.append(tup)
        print('Symbols succesfully generated')

        print(tuples)

# scrap_djia()
# scrap_us500()
# scrap_dax()
# scrap_nasdaq100()
# scrap_ftse100()
# scrap_cac40()
# scrap_smi()
scrap_wig20()
