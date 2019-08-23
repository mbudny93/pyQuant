import sys
import requests
import lxml.html

def getContent(url):
    try:
        res = requests.get(url)
    except:
        sys.exit('FATAL ERROR: Unable to connect to url ...')

    return lxml.html.fromstring(res.content)

def format(tickers, securities, sectors):
        output = []
        for ticker, security, sector in zip(tickers, securities, sectors):
            tuple = (ticker.rstrip(), security.rstrip(), sector.rstrip())
            output.append(tuple)
        if not output:
            sys.exit('FATAL ERROR: Empty list generated ...')
        print('Symbols succesfully generated')
        return output

# def format(tickers, securities):
        # output = []
        # for ticker, security in zip(tickers, securities):
            # tuple = (ticker.rstrip(), security.rstrip(), 'N/A')
            # output.append(tuple)
        # if not output:
            # sys.exit('FATAL ERROR: Empty list generated ...')
        # print('Symbols succesfully generated')
        # return output

def scrap_djia():
    url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
    cont = getContent(url)
    tickers = cont.xpath('//table[2]//td[3]//text()')[0:-1:2]
    securities = cont.xpath('//table[2]//td[1]//text()')[0:-1:2]
    sectors = cont.xpath('//table[2]//td[4]//text()')[0:-1:2]
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_us500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    cont = getContent(url)
    tickers = cont.xpath('//table[1]//td[1]//text()')[0:-1:2]
    securities = cont.xpath('//table[1]//td[2]//text()')
    sectors = cont.xpath('//table[1]//td[4]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_dax():
    url = 'https://en.wikipedia.org/wiki/DAX'
    cont = getContent(url)
    tickers = cont.xpath('//table[3]//td[4]//text()')
    securities = cont.xpath('//table[3]//td[2]//text()')
    sectors = cont.xpath('//table[3]//td[3]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_ftse100():
    url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
    cont = getContent(url)
    tickers = cont.xpath('//table[3]//td[2]//text()')
    securities = cont.xpath('//table[3]//td[1]//text()')
    sectors = cont.xpath('//table[3]//td[3]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_cac40():
    url = 'https://en.wikipedia.org/wiki/CAC_40'
    cont = getContent(url)
    tickers = cont.xpath('//table[3]//td[3]//text()')
    securities = cont.xpath('//table[3]//td[1]//text()')
    sectors = cont.xpath('//table[3]//td[2]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_wig20():
    url = 'https://pl.wikipedia.org/wiki/WIG20'
    cont = getContent(url)
    tickers = cont.xpath('//table[1]//td[2]//text()')
    securities = cont.xpath('//table[1]//td[1]//text()')[0:-1:2]
    sectors = cont.xpath('//table[1]//td[3]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res

def scrap_nasdaq100():
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    cont = getContent(url)
    tickers = cont.xpath('//table[3]//td[2]//text()')
    securities = cont.xpath('//table[3]//td[1]//text()')
    res = format(tickers, securities, sectors)
    print(res)
    return res
