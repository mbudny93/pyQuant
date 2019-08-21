from blob import *

DbSupervisor.establishConnection()

ds1 = US500('spy')
ds1.fetchHistoricalQuotes()
ds1.update()
