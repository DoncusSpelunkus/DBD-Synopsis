from pymongo import MongoClient
import json
import os
import time

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Define the database
db = client["mongo"]

# Start the timer
start_time = time.time()

# Define the collections
user_primary_collection = db["User_Primary"]
session_user_data_collection = db["Session_User_data"]
user_total_data_collection = db["User_Total_data"]

# Check if collections are empty
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

        # Create indexes for faster querying
        user_primary_collection.create_index("age")
        session_user_data_collection.create_index("UserId")

        # Extract session user data and total data from each user and insert into respective collections
        for user in all_users:
            user_id = user["user_id"]
            session_user_data_collection.insert_many(user["session_user_data"])
            user_total_data_collection.insert_one(user["total_data"])

        print("Data imported successfully.")
    else:
        print(f"JSON file '{json_file_path}' not found.")

# Query to get all users between 18 and 21 years old
users_between_18_and_21 = user_primary_collection.find({"age": {"$gte": 18, "$lte":21}})

# List to store the results
user_sessions = []

# Fetch session lifetime for each user
for user in users_between_18_and_21:
    user_id = user["user_id"]
    age = user["age"]
    sessions = session_user_data_collection.find({"UserId": user_id}, {"SessionLifeTime": 1, "_id": 0})
    for session in sessions:
        user_sessions.append({"UserId": user_id, "Age": age, "SessionLifeTime": session["SessionLifeTime"]})

# Print the results
for user_session in user_sessions:
    print(user_session)

# Calculate and print the elapsed time
elapsed_time = time.time() - start_time
print("Elapsed Time:", elapsed_time, "seconds")