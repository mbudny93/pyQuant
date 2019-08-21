import time
import pymysql

from query import Query

class DbSupervisor:

    connection = None

    @staticmethod
    def establishConnection():
        try:
            start = time.time()
            connection = pymysql.connect(host='localhost', user='admin', password='admin')
            end = time.time()
            print('Succesfully connected to local database in', end-start, 'seconds.')
            DbSupervisor.connection = connection
        except:
            DbSupervisor.connection.close()
            sys.exit('FATAL ERROR: Unable to connect to local database.')

    @staticmethod
    def connectToDatabase(dbName):
        try:
            with DbSupervisor.connection.cursor() as cursor:
                start = time.time()
                DbSupervisor.cursor.execute(Query(DbSupervisor.connection).useDatabase(dbName))
                end = time.time()
                print('Successfully connected to database', dbName, 'in', end-start, 'seconds')
        except:
            sys.exit('FATAL ERROR: Unable to connect to database', dbName)

    @staticmethod
    def checkIfDatabaseExists(dbName):
        try:
            with DbSupervisor.connection.cursor() as cursor:
                return cursor.execute(Query.checkIfDatabaseExists(dbName))
        except:
            DbSupervisor.connection.close()
            sys.exit('FATAL ERROR: Unable to perform simple query')
