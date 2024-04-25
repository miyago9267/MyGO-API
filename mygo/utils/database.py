
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Mongo:
    def __init__(self, uri):
        client = MongoClient(uri, server_api=ServerApi('1'))

        self.db = client[db_name]
        self.collection = self.db[collection_name]

    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def insert_one(self, data):
        return self.collection.insert_one(data)