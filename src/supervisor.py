import time
import pymysql
import sys

from query import Query

class DbSupervisor:

    connection = None

    @staticmethod
    def establishMySqlConnection():
        try:
            start = time.time()
            connection = pymysql.connect(host='localhost', user='admin', password='admin')
            end = time.time()
            DbSupervisor.connection = connection
            print('Succesfully connected to local database in', end-start, 'seconds.')
        except:
            sys.exit('FATAL ERROR: Unable to connect to local database.')

    @staticmethod
    def connectToDatabase(dbName):
        try:
            with DbSupervisor.connection.cursor() as cursor:
                start = time.time()
                cursor.execute(Query.useDatabase(dbName))
                end = time.time()
                print('Successfully connected to database', dbName, 'in', end-start, 'seconds')
        except(pymysql.err.InternalError):
             raise pymysql.err.InternalError

    @staticmethod
    def databaseExists(dbName):
        with DbSupervisor.connection.cursor() as cursor:
            return cursor.execute(Query.checkIfDatabaseExists(dbName))

