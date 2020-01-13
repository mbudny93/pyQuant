from supervisor import DbSupervisor
from controller import Controller
from dataset import *

import sys
import shutil

class Handler:

    @staticmethod
    def init():
        print('Inside init')
        if Controller.datasets:
            sys.exit('Existing datasets detected, use --purge.')
        print('No datasets detected, initializing default datasets...')
        Controller.generateDatasets()
        for ds in Controller.datasets:
            ds.create()
        Controller.saveDatasets()

    @staticmethod
    def purge():
        print('Inside purge')
        for ds in Controller.datasets:
            print(ds.getName())
            ds.remove()
        Controller.datasets = []
        Controller.purgeDatasets()
        shutil.rmtree(Controller.dump_dir)

    @staticmethod
    def create(params):
        print('Inside create')
        if len(params) == 1 and params[0] == '*':
            print('allhu akbar!')
        for x in params:
            print(x)

    @staticmethod
    def remove(params):
        print('Inside remove')
        print(params)

    @staticmethod
    def fill(params):
        print('Inside fill')
        print(params)

    @staticmethod
    def update(params):
        print('Inside update')
        print(params)

    @staticmethod
    def dblist():
        print('Inside dblist')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('show databases;')
            result = cursor.fetchall()
            for res in result:
                print(res)

    @staticmethod
    def sqlstatus():
        print('Inside sqlstatus')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('status;')
            result = cursor.fetchall()
            for res in result:
                print(res)

    @staticmethod
    def sqlusers():
        print('Inside sqlusers')
        with DbSupervisor.connection.cursor() as cursor:
            cursor.execute('select user from mysql.user;')
            result = cursor.fetchall()
            for res in result:
                print(res)
