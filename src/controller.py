from dataset import *
import pickle
import os

class Controller:

    datasets = None
    main_dir = None
    dump_dir = None

    def __init__(self):
        print('Main controller created')

    def generateDatasets(self):
        self.datasets = [
            US500('spy'),
            DAX30('dax'),
            FTSE100('ftse'),
            WIG20('wig')
        ]

    def saveDatasets(self):
        for ds in self.datasets:
            file_name = self.dump_dir + ds.getName() + '.pickle'
            with open(file_name, 'wb') as file:
                pickle.dump(ds, file)

    def loadDatasets(self):
        print('LOADING DATASETS.............................')
        deserialized_datasets = []
        dump_files = os.listdir(self.dump_dir)
        print(dump_files)
        for file in dump_files:
            file_name = self.dump_dir + '/' + file
            print(file_name)
            with open(file_name, 'rb') as f:
                loaded_obj = pickle.load(f)
                deserialized_datasets.append(loaded_obj)
        return deserialized_datasets


        # for ds in self.datasets:
            # file_name = '../.dump/' + ds.getName() + '.pickle'
            # with open(file_name) as file:
                # loaded_obj = pickle.load(file)

