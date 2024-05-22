from pymongo import MongoClient

class MyMongoFactory:
    @staticmethod
    def create_client():
        return MyMongoClient("mongodb://localhost:27017/")
    
class MyMongoClient:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.client = None

    def __repr__(self):
        return f"MyMongoClient(connection_string='{self.connection_string}')"
    
    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection to see if it works
            if self.client.list_database_names():
                print(f"Connected to MongoDB at {self.connection_string}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
    
    def getDb(self):
        return self.client["mongo"]
    
    def getLifetimeByDate(self, start_date, end_date):
        db = self.getDb()
        users_between_18_and_21 = db.user_primary_collection.find({"age": {"$gte": 18, "$lte": 21}})
        print(users_between_18_and_21)
       
        return list(users_between_18_and_21)