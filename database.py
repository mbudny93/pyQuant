import pymysql

class Database:
    def __init__(self, db_name):
        self.name = db_name
        connection = pymysql.connect(host='localhost', user='admin', password='admin')

    def drop(self):
        return True

    def connect(self, )

