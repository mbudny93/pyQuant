from dataset import *
from supervisor import *

DbSupervisor.establishConnection()

ds1 = US500('spy')
ds2 = DAX30('dax')
ds3 = FTSE100('ftse')
ds4 = WIG20('wig20')

# ds1.fill()
# ds1.update()
