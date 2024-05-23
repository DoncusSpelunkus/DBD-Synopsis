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
        session_data = db.get_collection("Session_User").find({"SessionStartDate": {"$gte": start_date, "$lte": end_date}},{"SessionLifeTime": 1, "_id": 0})
        result = []
        # Check if any users were found
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No users found between 18 and 21 years old in the specified date range.")
            
        return list(result)
    
    def getSessionSpecificWithUser(self, userId, sessionId):
        db = self.getDb()
        session_data = db.get_collection("Session_User").find({"UserId": userId, "SessionId": sessionId},{"SessionLifeTime": 1, "_id": 0})
        result = []
        # Check if any users were found
        if session_data:
            for session in session_data:
                result.append(session)

        else:
            print("No users found between 18 and 21 years old in the specified date range.")
            
        return list(result)
    
    def getAllSessions(self):
        db = self.getDb()
        session_data = db.get_collection("Session_User").find({},{"SessionLifeTime": 1, "_id": 0})
        result = []
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No users found between 18 and 21 years old in the specified date range.")
        
        return list(result)