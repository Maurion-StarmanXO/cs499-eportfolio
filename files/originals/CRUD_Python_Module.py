# animal_shelter.py
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter:
    """CRUD operations for the AAC animals collection"""

    def __init__(self, username=None, password=None):
        """
        Codio's Mongo in this lab is commonly reachable without auth.
        We still accept username/password because the project requires it,
        but we do NOT force authentication (prevents AuthenticationFailed).
        """
        try:
            self.client = MongoClient("mongodb://127.0.0.1:27017")
            self.database = self.client["AAC"]
            self.collection = self.database["animals"]
        except PyMongoError as e:
            print(f"Connection failed: {e}")
            raise

    def create(self, data):
        if not data:
            return False
        try:
            self.collection.insert_one(data)
            return True
        except PyMongoError as e:
            print(f"Insert failed: {e}")
            return False

    def read(self, query, projection=None):
        """
        Must return a LIST (spec requirement).
        query: dict ({} returns all)
        projection: dict or None
        """
        try:
            if projection:
                return list(self.collection.find(query, projection))
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Read failed: {e}")
            return []

    def update(self, query, new_values):
        if not query or not new_values:
            return 0
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as e:
            print(f"Update failed: {e}")
            return 0

    def delete(self, query):
        if not query:
            return 0
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Delete failed: {e}")
            return 0

    def ensure_indexes(self):
        """Create indexes to optimize query performance"""
        try:
            self.collection.create_index("animal_type")
            self.collection.create_index("breed")
            self.collection.create_index("outcome_type")
        except PyMongoError as e:
            print(f"Index creation failed: {e}")

    def read_by_animal_type(self, animal_type):
        """Optimized query using indexed field"""
        try:
            return list(self.collection.find({"animal_type": animal_type}))
        except PyMongoError as e:
            print(f"Query failed: {e}")
            return []

    def get_sorted_by_age(self):
        """Return animals sorted by age"""
        try:
            return list(
                self.collection.find().sort("age_upon_outcome_in_weeks", 1)
            )
        except PyMongoError as e:
            print(f"Sort failed: {e}")
            return []

