
# abstraction layer over database
class Dataset:
    def __init__(self, name):
        self.name = name
        self.database = {}
        self.mambers = []

    def createDatabase(self):
        pass

    def dropDatabase(self):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def generateTickersList(self):
        pass

    def getTickersList(self):
        pass

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        pass

us500 = Dataset('us500')
us500.init()
us500.update()

