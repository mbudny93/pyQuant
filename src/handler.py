from dataset import datasets

class Handler:
    @staticmethod
    def init():
        print('Inside init')
        for ds in datasets:
            print(ds.getName())

    @staticmethod
    def purge():
        print('Inside purge')
        for ds in datasets:
            print(ds.getName())

    @staticmethod
    def create(params):
        print('Inside create')
        if len(params) == 1 and params[0] == '*':
            print('allhu akbar!')
        for x in params:
            print(x)

    @staticmethod
    def remove(params):
        print('Inside remove')
        print(params)

    @staticmethod
    def fill(params):
        print('Inside fill')
        print(params)

    @staticmethod
    def update(params):
        print('Inside update')
        print(params)

