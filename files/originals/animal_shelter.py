# animal_shelter.py
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from CRUD_Python_Module import AnimalShelter as EnhancedShelter


class AnimalShelter:
    """
    CRUD helper for the AAC database.

    Note: In the Codio CS-340 environment, MongoDB commonly runs with
    access control disabled. The assignment still wants you to pass
    username/password when instantiating the class, but the connection
    here uses localhost without authentication to match the environment.
    """

    def __init__(self, username: str = None, password: str = None,
                 host: str = "localhost", port: int = 27017,
                 db_name: str = "AAC", collection_name: str = "animals"):

        self.client = MongoClient(f"mongodb://{host}:{port}/")
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]
        self.enhanced = EnhancedShelter()
        self.enhanced.ensure_indexes()

    def create(self, data: dict) -> bool:
        if not data:
            raise ValueError("create() requires a non-empty dict")

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError:
            return False

    def read(self, query: dict = None) -> list:
        if query is None:
            return self.enhanced.read({})

        # Optimization: use indexed query if filtering by animal_type
        if "animal_type" in query:
            return self.enhanced.read_by_animal_type(query["animal_type"])

        return self.enhanced.read(query)

    def update(self, query: dict, new_values: dict) -> int:
        if not query or not new_values:
            raise ValueError("update() requires query and new_values dicts")

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError:
            return 0

    def delete(self, query: dict) -> int:
        if not query:
            raise ValueError("delete() requires a query dict")

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError:
            return 0
