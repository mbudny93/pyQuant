from dataset import *
from supervisor import *

DbSupervisor.establishConnection()

datasets = [
    US500('spy'),
    DAX30('dax'),
    FTSE100('ftse'),
    WIG20('wig')
]

for ds in datasets:
    ds.create()
    ds.fill()
    ds.update()

