from pymongo import MongoClient
from tabulate import tabulate
import time


class MyMongoFactory:
    @staticmethod
    def create_client(dbName="Index"):
        return MyMongoClient("mongodb://localhost:27017/", dbName)


class MyMongoClient:
    def __init__(self, connection_string: str, dbName):
        self.connection_string = connection_string
        self.client = None
        self.dbName = dbName

    def __repr__(self):
        return f"MyMongoClient(connection_string='{self.connection_string}')"

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)

        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")

    def getDb(self):
        return self.client[self.dbName]

    def getLifetimeByDate(self, start_date, end_date):
        db = self.getDb()
        session_data = db.get_collection("User_Primary").find(
            {"Session_User_Data.SessionStartDate": {"$gte": start_date, "$lte": end_date}}, {"Session_User_Data.SessionLifeTime": 1, "_id": 0})
        result = []
        # Check if any users were found
        if session_data:
            for session in session_data:
                result.append(session)
                
        if len(result) == 0:
            raise Exception("No users found between the specified date range.")
            
        return list(result)

    def getSessionSpecificWithUser(self, userId, sessionId):

        db = self.getDb()
        session_data = db.get_collection("User_Primary").find({"User_Id": userId, "Session_User_Data.SessionId": sessionId},{"Session_User_Data.SessionLifeTime": 1, "_id": 0})
        
        result = []
        # Check if any users were found
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No session found with the specified userId and sessionId.")

        if len(result) == 0:
            raise Exception("No session found with the specified userId and sessionId.")
            
        return result

    def getAllSessions(self):
        db = self.getDb()
        session_data = db.get_collection("User_Primary").find({}, {"_id": 0})
        result = []
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No users found between 18 and 21 years old in the specified date range.")

        if len(result) == 0:
            raise Exception("No sessions found.")
            
        return list(result)

    def get_users_by_website(self, website_url):
        db = self.getDb()
        
        user_data = db.get_collection("User_Primary").find({"Total_Data.ListOfUrls": website_url}, {"_id": 0})
        result = []
        if user_data:
            for user in user_data:
                result.append(user)
        else:
            print("No users found who visited the specified website.")
        
        if len(result) == 0:
            raise Exception("No users found who visited the specified website.")
            
        return list(user_data)
    
    def create_user(self, user):
        try:
            db = self.getDb()
            
            user_collection = db.get_collection("User_Primary")
            
            result = user_collection.insert_one(user)
            
            if result.inserted_id is not None:
                return user
            else:
                raise Exception("User creation failed.")
        except Exception as e:
            print(e)

    
    def delete_user(self, user_id):
        db = self.getDb()
        user_collection = db.get_collection("User_Primary")
        user_collection.delete_one({"User_Id": user_id})
        
    def remove_test_users(self, users):
        try:
            db = self.getDb()
            user_collection = db.get_collection("User_Primary")
            for user in users:
                user_collection.delete_one({"User_Id": user["User_Id"]})
        except Exception as e:
            print(e)
            raise e
        
    def get_a_website(self):
        try:
            db = self.getDb()
            user_collection = db.get_collection("User_Primary")
            user = user_collection.find_one()
            return user["Total_Data"]["ListOfUrls"][0]
        except Exception as e:
            print(e)
            raise e
        