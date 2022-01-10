import pymongo

class Database:
    def __init__(self, link="mongodb://localhost:27017/", db_name=''):
        '''initialise database'''
        # print("connecting to:", link)
        self.client = pymongo.MongoClient(link)
        self.db = self.client[db_name]