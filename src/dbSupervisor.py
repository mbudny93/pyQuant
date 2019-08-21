
class DbSupervisor:
    connection = {}
    cursor = {}

    @staticmethod
    def establishConnection():
        try:
            start = time.time()
            connection = pymysql.connect(host='localhost', user='admin', password='admin')
            end = time.time()
            print('Succesfully connected to localDb in', end-start, 'seconds.')
            DbSupervisor.connection = connection
            DbSupervisor.cursor = connection.cursor()
        except:
            sys.exit('FATAL ERROR: Unable to connect to localDb')

    @staticmethod
    def connectToDatabase(dbName):
        try:
            start = time.time()
            DbSupervisor.cursor.execute(Query(DbSupervisor.connection).useDatabase(dbName))
            end = time.time()
            print('Successfully connected to database:', dbName, 'in', end-start, 'seconds')
        except:
            sys.exit('FATAL ERROR: Unable to connect to database', dbName)
