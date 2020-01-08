import sys
import os
import pytest
import pymysql

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from supervisor import DbSupervisor
from database import Database

def test_connect_to_mysql():
    assert(DbSupervisor.connection is None)
    DbSupervisor.establishMySqlConnection()
    assert(DbSupervisor.connection is not None)

def test_if_database_exists():
    DbSupervisor.establishMySqlConnection()
    fake_db_name = "dupsaxa"
    assert(not DbSupervisor.databaseExists(fake_db_name))

def test_create_database():
    DbSupervisor.establishMySqlConnection()
    db_name = "test_db"
    assert(not DbSupervisor.databaseExists(db_name))
    test_db = Database(db_name).createDatabase()
    assert(DbSupervisor.databaseExists(db_name))
    test_db.dropDatabase()
    assert(not DbSupervisor.databaseExists(db_name))

def test_connect_to_nonexistent_database():
    DbSupervisor.establishMySqlConnection()
    fake_db_name = "dupsaxa"
    assert(not DbSupervisor.databaseExists(fake_db_name))
    with pytest.raises(pymysql.err.InternalError):
        DbSupervisor.connectToDatabase(fake_db_name)

def test_connect_to_database():
    DbSupervisor.establishMySqlConnection()
    db_name = "test_db"
    assert(not DbSupervisor.databaseExists(db_name))
    test_db = Database(db_name).createDatabase()
    assert(DbSupervisor.databaseExists(db_name))
    DbSupervisor.connectToDatabase(db_name)
    test_db.dropDatabase()
    assert(not DbSupervisor.databaseExists(db_name))
