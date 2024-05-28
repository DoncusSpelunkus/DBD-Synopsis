from pymongo import MongoClient
import os
import json

class ContextBuild:
    @staticmethod
    def rebuildIndexedDb():
        client = MongoClient("mongodb://localhost:27017")
        db = client["Index"]
        
        db.drop_collection("User_Primary")

        user_primary_collection = db["User_Primary"]

        user_primary_collection.create_index([("User_Id", 1)], unique=True)
        user_primary_collection.create_index([("Session_User_Data.SessionStartDate", 1)])
        user_primary_collection.create_index([("Session_User_Data.SessionId", 1), ("User_Id", 1)])
        user_primary_collection.create_index([("Total_Data.TotalId", 1)])
        user_primary_collection.create_index([("Total_Data.ListOfUrls", 1)])
        
        for index in user_primary_collection.list_indexes():
            print(index)
        
        
        try:
            if user_primary_collection.count_documents({}):
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
                    
                    print("Data imported successfully.")
                else:
                    print(f"JSON file '{json_file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
            db.drop_collection("User_Primary")
            
    @staticmethod
    def rebuildNonIndexedDb():
        client = MongoClient("mongodb://localhost:27017")
        db = client["NoIndex"]
        
        db.drop_collection("User_Primary")
        
        user_primary_collection = db["User_Primary"]
        
        try:
            if user_primary_collection.count_documents({}):
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


                    print("Data imported successfully.")
                else:
                    print(f"JSON file '{json_file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
            db.drop_collection("User_Primary")
            
    @staticmethod
    def deleteDb(dbName):
        client = MongoClient("mongodb://localhost:27017")
        client.drop_database(dbName)
        print("Databases deleted successfully.")