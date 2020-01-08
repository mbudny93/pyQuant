import sys
import os
import pytest
import pymysql

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from supervisor import DbSupervisor
from database import Database
from query import Query

DbSupervisor.establishMySqlConnection()
# fake_db = 'sdgdhfdfhdb'
fake_db = 'test'
query = Query.checkIfDatabaseExists(fake_db)
print(query)
result = DbSupervisor.connection.cursor().execute(query)
print(result)

