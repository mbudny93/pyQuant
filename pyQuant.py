#!/usr/bin/env python

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src")

print(sys.path)

from dataset import *
from supervisor import *

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output', action='store_true', help="shows output")
parser.add_argument('-t', '--toutput', action='store_true', help="shows output")
parser.add_argument('-n', '--noutput', action='store_true', help="shows output")

args = parser.parse_args()

if args.output:
    print("This is some output")
elif args.toutput:
    print("This is some toutput")
elif args.noutput:
    print("This is some noutput")
else:
    print("dupa")


#=======================================================================================

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
