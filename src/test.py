from dbSupervisor import DbSupervisor
from blob import Database, Dataset, US500, Forex

DbSupervisor.establishConnection()

ds1 = US500('spy')
ds1.fetchHistoricalQuotes()
ds1.update()
