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
        session_data = db.get_collection("Session_User").find(
            {"SessionStartDate": {"$gte": start_date, "$lte": end_date}}, {"SessionLifeTime": 1, "_id": 0})
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
        session_data = db.get_collection("Session_User").find({"UserId": userId, "SessionId": sessionId},
                                                              {"SessionLifeTime": 1, "_id": 0})
        result = []
        # Check if any users were found
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No session found with the specified userId and sessionId.")

        return result

    def getAllSessions(self):
        db = self.getDb()
        session_data = db.get_collection("Session_User").find({}, {"_id": 0})
        result = []
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No users found between 18 and 21 years old in the specified date range.")

        return list(result)


def getLifetimeByDate(self, start_date, end_date):
    db = self.getDb()
    pipeline = [
        {"$match": {"SessionStartDate": {"$gte": start_date, "$lte": end_date}}},
        {"$project": {"SessionLifeTime": 1, "_id": 0}}
    ]
    session_data = db.get_collection("Session_User").aggregate(pipeline)
    return list(session_data)


def get_users_by_website(self, website_url):
    db = self.getDb()
    pipeline = [
        {"$match": {"Listofurls": {"$elemMatch": {"$eq": website_url}}}},
        {"$project": {"UserId": 1, "_id": 0}}
    ]
    user_data = db.get_collection("User_Total").aggregate(pipeline)
    result = []
    if user_data:
        for user in user_data:
            result.append(user)
    else:
        print("No users found who visited the specified website.")
    return list(user_data)
