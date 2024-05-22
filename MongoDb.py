from pymongo import MongoClient
import datetime

# Replace with your MongoDB connection string
client = MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["UserMetrics"]

# Define the collections (tables)
user_primary_collection = db["User_Primary"]
session_user_data_collection = db["Session_User_data"]
user_total_data_collection = db["User_Total_data"]

# Define the documents (rows) for each collection with actual sample data
user_primary_document = {
    "name": "John",
    "lastName": "Doe",
    "age": 30,
    "primeryld": 1,
}

session_user_data_document = {
    "Sessionld": 1,
    "Userld": 1,
    "SessionSearchAmount": 5,
    "SessionLinkClicks": 10,
    "SessionLifeTime": 3600,
    "SessionStartDate": datetime.datetime.now(),
    "SessionLinks": ["http://example.com", "http://example2.com"],
}

user_total_data_document = {
    "Totalld": 1,
    "Userld": 1,
    "TotalLinkClickAmount": 15,
    "ListOfUrls": ["http://example.com", "http://example2.com", "http://example3.com"],
}

# Create the collections if they don't exist yet
user_primary_collection.create_index([("primeryld", 1)], unique=True)
session_user_data_collection.create_index([("Sessionld", 1)], unique=True)
user_total_data_collection.create_index([("Totalld", 1)], unique=True)

# Insert the documents into the collections
user_primary_collection.insert_one(user_primary_document)
session_user_data_collection.insert_one(session_user_data_document)
user_total_data_collection.insert_one(user_total_data_document)

# Print the inserted documents to verify
print("User Primary Document:")
print(user_primary_collection.find_one({"primeryld": 1}))

print("\nSession User Data Document:")
print(session_user_data_collection.find_one({"Sessionld": 1}))

print("\nUser Total Data Document:")
print(user_total_data_collection.find_one({"Totalld": 1}))
