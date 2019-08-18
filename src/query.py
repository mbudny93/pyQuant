
class Query:
    def __init__(self, connection):
        self.connection = connection

    def createDatabase(self, dbname):
        query = 'create database %s;'%(dbname)
        return query

    def useDatabase(self, dbname):
        query = 'use %s;'%(dbname)
        return query

    def dropDatabase(self, dbname):
        query = 'drop database %s;'%(dbname)
        return query

    def createTables(self, symbol_table_name, price_table_name):
        symbol_table = "CREATE TABLE `%s` (\
          `id` int NOT NULL AUTO_INCREMENT,\
          `ticker` varchar(32) NOT NULL,\
          `name` varchar(255) NULL,\
          `sector` varchar(255) NULL,\
          PRIMARY KEY (`id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"%symbol_table_name

        price_table = "CREATE TABLE `%s` (\
          `id` int NOT NULL AUTO_INCREMENT,\
          `symbol_id` int NOT NULL,\
          `price_date` datetime NOT NULL,\
          `open_price` decimal(19,4) NULL,\
          `high_price` decimal(19,4) NULL,\
          `low_price` decimal(19,4) NULL,\
          `close_price` decimal(19,4) NULL,\
          `volume` bigint NULL,\
          PRIMARY KEY (`id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"%price_table_name

        return symbol_table, price_table

    def getTableColumnNames(self, db_name, table_name):
        query = ('SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE'
            '`TABLE_SCHEMA`=\'%s\' AND `TABLE_NAME`=\'%s\';')%(db_name, table_name)
        return query

    def insertSymbols(self, symbol_table_name, columns, values):
        query = 'INSERT INTO %s (%s) VALUES %s'%(symbol_table_name, columns, values)
        return query

    def getTickers(self, symbol_table_name):
        query = 'SELECT id, ticker FROM %s'%(symbol_table_name)
        return query

    def insertQuotes(self, price_table_name, columns):
        query = 'INSERT INTO %s (%s) VALUES '%(price_table_name, columns)
        return query

    def getQuotes(self, ticker, symbol_table_name, price_table_name):
        query = ('SELECT %s.price_date,'
                 '%s.open_price,'
                 '%s.high_price,'
                 '%s.low_price,'
                 '%s.close_price,'
                 '%s.volume '
                 'FROM %s INNER JOIN %s ON '
                 '%s.symbol_id = %s.id '
                 'WHERE %s.ticker = \'%s\' '
                 'ORDER BY %s.price_date ASC;'
                 '')%(price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      symbol_table_name,
                      price_table_name,
                      price_table_name,
                      symbol_table_name,
                      symbol_table_name,
                      ticker, price_table_name);
        return query

    def getLastQuote(self, ticker, symbol_table_name, price_table_name, order):
        query = ('SELECT %s.price_date,'
                 '%s.open_price,'
                 '%s.high_price,'
                 '%s.low_price,'
                 '%s.close_price,'
                 '%s.volume '
                 'FROM %s INNER JOIN %s ON '
                 '%s.symbol_id = %s.id '
                 'WHERE %s.ticker = \'%s\' '
                 'ORDER BY %s.price_date %s '
                 'LIMIT 1;'
                 '')%(price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      price_table_name,
                      symbol_table_name,
                      price_table_name,
                      price_table_name,
                      symbol_table_name,
                      symbol_table_name,
                      ticker, price_table_name, order);
        return query
