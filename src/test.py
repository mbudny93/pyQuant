from dataset import *
from supervisor import *

DbSupervisor.establishMySqlConnection()

datasets = [
    US500('spy'),
    DAX30('dax'),
    FTSE100('ftse'),
    WIG20('wig')
]

for ds in datasets:
    # print(ds.getName())
    ds.use()
    # ds.create()
    # ds.fill()
    # ds.update()

