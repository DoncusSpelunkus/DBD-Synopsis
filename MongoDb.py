from pymongo import MongoClient
import datetime
# Replace the following with your MongoDB connection string
client = MongoClient("mongodb://localhost:27017/")

# Define the database
db = client["mongo"]

# Define the collections (classes)
user_primary_collection = db["User_Primary"]
session_user_data_collection = db["Session_User_data"]
user_total_data_collection = db["User_Total_data"]

# Define the documents (fields) for each collection
user_primary_document = {
    "name": str,
    "lastName": str,
    "age": int,
    "primeryld": int,
}

session_user_data_document = {
    "Sessionld": int,
    "Userld": int,
    "SessionSearchAmount": int,
    "SessionLinkClicks": int,
    "SessionLifeTime": int,
    "SessionStart date": datetime.datetime,
    "SessionLinks": list,
}

user_total_data_document = {
    "Totalld": int,
    "Userld": int,
    "Total link click amount": int,
    "List of urls": list,
}

# Create the collections if they don't exist yet
user_primary_collection.create_index([("primeryld", 1)], unique=True)
session_user_data_collection.create_index([("Sessionld", 1)], unique=True)
user_total_data_collection.create_index([("Totalld", 1)], unique=True)

# Insert sample data (optional)
user_primary_collection.insert_one(user_primary_document)
session_user_data_collection.insert_one(session_user_data_document)
user_total_data_collection.insert_one(user_total_data_document)

# Print the collections (for verification)
print(user_primary_collection.find_one())
print(session_user_data_collection.find_one())
print(user_total_data_collection.find_one())