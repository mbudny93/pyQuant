from dataset import *
import pickle
import os

class Controller:

    datasets = []
    main_dir = ''
    dump_dir = ''

    @staticmethod
    def setProjectDirs(m_dir, d_dir):
        Controller.main_dir = m_dir
        Controller.dump_dir = d_dir

    @staticmethod
    def generateDatasets():
        default_datasets = [
            US500('spy'),
            DAX30('dax'),
            FTSE100('ftse'),
            WIG20('wig')
        ]
        Controller.datasets = default_datasets

    @staticmethod
    def saveDatasets():
        for ds in Controller.datasets:
            file_name = Controller.dump_dir + '/' + ds.getName() + '.pickle'
            print(file_name)
            with open(file_name, 'wb') as file:
                pickle.dump(ds, file)

    @staticmethod
    def purgeDatasets():
        for ds in Controller.datasets:
            pass

    @staticmethod
    def loadDatasets():
        print('LOADING DATASETS...')
        deserialized_datasets = []
        dump_files = os.listdir(Controller.dump_dir)
        for file in dump_files:
            file_name = Controller.dump_dir + '/' + file
            with open(file_name, 'rb') as f:
                loaded_obj = pickle.load(f)
                deserialized_datasets.append(loaded_obj)
        print('Found: ' + str(len(deserialized_datasets)) + ' datasets...')
        Controller.datasets = deserialized_datasets
