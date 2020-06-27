from pymongo import MongoClient


class Bet365Mongo(object):
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client['bet365_database']
        self.collection = self.db['game_data']

    def insert_game_data(self, data):
        self.collection.insert_one(data)