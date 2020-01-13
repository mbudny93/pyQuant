import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from controller import *

test_main_dir = os.path.dirname(os.path.realpath(__file__))
test_dump_dir = test_main_dir + '/.dump/'


def clean_dump_dir():
    if os.path.exists(test_dump_dir):
        shutil.rmtree(test_dump_dir)
    os.makedirs(test_dump_dir)
    assert not (os.listdir(test_dump_dir))


def test_serialize_datasets():
    clean_dump_dir()
    controller = Controller()
    controller.main_dir = test_main_dir
    controller.dump_dir = test_dump_dir

    controller.datasets =  [ US500('spy'), DAX30('dax'), FTSE100('ftse'), WIG20('wig') ]
    controller.saveDatasets()

    assert (len(os.listdir(test_dump_dir)) == len(controller.datasets))

def test_deserialize_datasets():
    clean_dump_dir()
    controller = Controller()
    controller.main_dir = test_main_dir
    controller.dump_dir = test_dump_dir

    controller.datasets =  [ US500('spy'), DAX30('dax'), FTSE100('ftse'), WIG20('wig') ]
    controller.saveDatasets()
    result = controller.loadDatasets()
    assert(result == controller.datasets)
