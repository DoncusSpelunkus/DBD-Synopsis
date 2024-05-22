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
    "FirstName": "John",
    "lastName": "Doe",
    "age": 30,
    "UserId": 1,
}

session_user_data_document = {
    "SessionId": 1,
    "UserId": 1,
    "SessionSearchAmount": 5,
    "SessionLinkClicks": 10,
    "SessionLifeTime": 3600,
    "SessionStart": datetime.datetime.now(),  # Field to be indexed with TTL
    "SessionLinks": ["http://example.com", "http://example2.com"],
}

user_total_data_document = {
    "TotalId": 1,
    "UserId": 1,
    "TotalLinkClickAmount": 15,
    "ListOfUrls": ["http://example.com", "http://example2.com", "http://example3.com"],
}

# Create indexes for `User_Primary`
user_primary_collection.create_index([("UserId", 1)], unique=True)  # Unique index on `UserId` in ascending order
user_primary_collection.create_index([("age", 1), ("UserId", 1)])  # Composite index on `age` and `UserId` in ascending order

# Create indexes for `Session_User_data`
session_user_data_collection.create_index([("SessionId", 1)], unique=True)  # Unique index on `SessionId` in ascending order
session_user_data_collection.create_index([("UserId", 1), ("SessionLinkClicks", 1)])  # Composite index on `UserId` and `SessionLinkClicks` in ascending order
session_user_data_collection.create_index([("SessionStart", 1)])  # Index on `SessionStart` in ascending order

# Drop the existing index on `SessionStart` if it exists
existing_indexes = session_user_data_collection.index_information()
if "SessionStart_1" in existing_indexes:
    session_user_data_collection.drop_index("SessionStart_1")

# Create a TTL index on `SessionStart` with a 30-day expiration (example)
session_user_data_collection.create_index([("SessionStart", 1)], expireAfterSeconds=30*24*60*60)

# Create indexes for `User_Total_data`
user_total_data_collection.create_index([("TotalId", 1)], unique=True)  # Unique index on `TotalId` in ascending order
user_total_data_collection.create_index([("UserId", 1), ("TotalLinkClickAmount", 1)])  # Composite index on `UserId` and `TotalLinkClickAmount` in ascending order

# Insert the documents into the collections
user_primary_collection.insert_one(user_primary_document)
session_user_data_collection.insert_one(session_user_data_document)
user_total_data_collection.insert_one(user_total_data_document)

# Print the inserted documents to verify
print("User Primary Document:")
print(user_primary_collection.find_one({"UserId": 1}))

print("\nSession User Data Document:")
print(session_user_data_collection.find_one({"SessionId": 1}))

print("\nUser Total Data Document:")
print(user_total_data_collection.find_one({"TotalId": 1}))

# Verify the created indexes
print("\nIndexes on User_Primary collection:")
print(user_primary_collection.index_information())

print("\nIndexes on Session_User_data collection:")
print(session_user_data_collection.index_information())

print("\nIndexes on User_Total_data collection:")
print(user_total_data_collection.index_information())
