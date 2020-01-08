from dbSupervisor import DbSupervisor
from dataset      import Dataset, US500, Forex
from database     import Database

DbSupervisor.establishConnection()

ds1 = US500('spy')
ds1.fetchHistoricalQuotes()
ds1.update()
