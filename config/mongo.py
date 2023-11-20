from pymongo import MongoClient

# from bson.binary import UuidRepresentation


class Mongo:
    def __init__(self, connection_string: str, db_name: str) -> None:
        self.mongo_client = MongoClient(connection_string, uuidRepresentation="standard")
        self.mongodb = self.mongo_client[db_name]

    def get_mongo_client(self):
        return self.mongo_client

    def create_index(self, collection_name, index, db_name=None):
        try:
            self.mongodb[collection_name].create_index(index)
        except Exception as e:
            raise e

    def insert_one(self, collection_name, data):
        try:
            self.mongodb[collection_name].insert_one(data)
        except Exception as e:
            raise e

    def insert_many(self, collection_name, data):
        try:
            self.mongodb[collection_name].insert_many(data)
        except Exception as e:
            raise e

    def find_one(self, collection_name, query):
        try:
            return self.mongodb[collection_name].find_one(query)
        except Exception as e:
            raise e

    def update_one(self, collection_name, query, data, upsert: bool = False):
        try:
            return self.mongodb[collection_name].update_one(query, data, upsert=upsert)
        except Exception as e:
            raise e

    def delete_one(self, collection_name, query):
        try:
            return self.mongodb[collection_name].delete_one(query)
        except Exception as e:
            raise e

    def perform_search(self, collection_name, query, index) -> list:
        try:
            return list(
                self.mongodb[collection_name].aggregate(
                    [
                        {
                            "$search": {
                                "index": index,
                                "text": {
                                    "query": query,
                                    "path": {
                                        "wildcard": "*",
                                    },
                                },
                            },
                        },
                    ]
                )
            )
        except Exception as e:
            raise e
