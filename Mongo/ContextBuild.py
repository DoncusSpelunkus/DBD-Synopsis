from pymongo import MongoClient
import os
import json

class ContextBuild:
    @staticmethod
    def rebuildIndexedDb():
        client = MongoClient("mongodb://localhost:27017")
        db = client["Index"]
        
        db.drop_collection("User_Primary")
        db.drop_collection("Session_User")
        db.drop_collection("User_Total")
        
        user_primary_collection = db["User_Primary"]
        session_user_data_collection = db["Session_User"]
        user_total_data_collection = db["User_Total"]
        
        
        user_primary_collection.create_index([("user_id", 1)], unique=True)
        session_user_data_collection.create_index([("SessionStartDate", 1)])
        session_user_data_collection.create_index([("SessionId", 1), ("UserId", 1)])
        user_total_data_collection.create_index([("TotalId", 1)], unique=True)
        
        list = session_user_data_collection.list_indexes()
        
        for index in list:
            print(index)
        
        try:
            if user_primary_collection.count_documents({}) > 0 or session_user_data_collection.count_documents({}) > 0 or user_total_data_collection.count_documents({}) > 0:
                print("Data already imported. Skipping import.")
            else:
                # Define path to JSON file
                json_file_path = "all_user_data_with_urls.json"

                # Check if JSON file exists
                if os.path.exists(json_file_path):
                    # Load data from JSON file
                    with open(json_file_path, "r") as json_file:
                        all_users = json.load(json_file)

                    # Insert user data into User_Primary collection
                    user_primary_collection.insert_many(all_users)

                    # Extract session user data and total data from each user and insert into respective collections
                    for user in all_users:
                        user_id = user["user_id"]
                        session_user_data_collection.insert_many(user["session_user_data"])
                        user_total_data_collection.insert_one(user["total_data"])

                    print("Data imported successfully.")
                else:
                    print(f"JSON file '{json_file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
            db.drop_collection("User_Primary")
            db.drop_collection("Session_User")
            db.drop_collection("User_Total")
            
    @staticmethod
    def rebuildNonIndexedDb():
        client = MongoClient("mongodb://localhost:27017")
        db = client["NoIndex"]
        
        db.drop_collection("User_Primary")
        db.drop_collection("Session_User")
        db.drop_collection("User_Total")
        
        user_primary_collection = db["User_Primary"]
        session_user_data_collection = db["Session_User"]
        user_total_data_collection = db["User_Total"]
        
        try:
            if user_primary_collection.count_documents({}) > 0 or session_user_data_collection.count_documents({}) > 0 or user_total_data_collection.count_documents({}) > 0:
                print("Data already imported. Skipping import.")
            else:
                # Define path to JSON file
                json_file_path = "all_user_data_with_urls.json"

                # Check if JSON file exists
                if os.path.exists(json_file_path):
                    # Load data from JSON file
                    with open(json_file_path, "r") as json_file:
                        all_users = json.load(json_file)

                    # Insert user data into User_Primary collection
                    user_primary_collection.insert_many(all_users)

                    # Extract session user data and total data from each user and insert into respective collections
                    for user in all_users:
                        user_id = user["user_id"]
                        session_user_data_collection.insert_many(user["session_user_data"])
                        user_total_data_collection.insert_one(user["total_data"])

                    print("Data imported successfully.")
                else:
                    print(f"JSON file '{json_file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
            db.drop_collection("User_Primary")
            db.drop_collection("Session_User")
            db.drop_collection("User_Total")
            
    @staticmethod
    def deleteDb(dbName):
        client = MongoClient("mongodb://localhost:27017")
        client.drop_database(dbName)
        print("Databases deleted successfully.")