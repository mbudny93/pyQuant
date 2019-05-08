from query import Query

class DataInserter:
    def __init__(self, database):
        self.database = database
    def insertSymbols(self):
        connection = self.database.connection
        cursor = connection.cursor()
        columns = self.database.getTableColumnNamesFormatted(self.database.symbol_table_name)
        table = self.database.symbol_table_name
        tickers = self.database.getTickersList()
        for symbol in tickers:
            values = symbol[0:-1]
            query = Query(connection).insertSymbols(table, columns, values)
            cursor.execute(query)
            print('Adding', symbol[1], '...')
        print('Database succesfully created.')

    def insertQuotes(self, vendor, quotes):
        connection = self.database.connection
        cursor = connection.cursor()
        columns = self.database.getTableColumnNamesFormatted(self.database.price_table_name)
        table = self.database.price_table_name
        preliminary_query = Query(connection).insertQuotes(table, columns)

        for day in quotes.values:
            d, o, h, l, c, v = vendor.adapt(day)
            values_query = '(\'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(str(d), str(o), str(h), str(l), str(c), str(v))
            query = preliminary_query + values_query
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            cursor.execute(query)
            # print(query)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        connection.commit()
