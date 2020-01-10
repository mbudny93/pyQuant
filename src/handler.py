from supervisor import DbSupervisor
from dataset import *

class Handler:

    def __init__(self):
        self.datasets_ = [
            US500('spy'),
            DAX30('dax'),
            FTSE100('ftse'),
            WIG20('wig')
        ]

    def init(self):
        print('Inside init')
        for ds in self.datasets_:
            ds.create()

    def purge(self):
        print('Inside purge')
        for ds in self.datasets_:
            print(ds.getName())
            ds.remove()

    def create(self, params):
        print('Inside create')
        if len(params) == 1 and params[0] == '*':
            print('allhu akbar!')
        for x in params:
            print(x)

    def remove(self, params):
        print('Inside remove')
        print(params)

    def fill(self, params):
        print('Inside fill')
        print(params)

    def update(self, params):
        print('Inside update')
        print(params)

    def dblist(self):
        print('Inside dblist')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('show databases;')
            result = cursor.fetchall()
            for res in result:
                print(res)

    def sqlstatus(self):
        print('Inside sqlstatus')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('status;')
            result = cursor.fetchall()
            for res in result:
                print(res)

    def sqlusers(self):
        print('Inside sqlusers')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('select user from mysql.user;')
            result = cursor.fetchall()
            for res in result:
                print(res)
