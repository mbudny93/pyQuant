from blob import *

DbSupervisor.establishConnection()

ds1 = US500('spy')
ds1.fill()
ds1.update()
