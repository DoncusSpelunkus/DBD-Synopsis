import json
import random
import string
import datetime


# Function to generate random URLs
def generate_random_urls(num_urls):
    urls = []
    for _ in range(num_urls):
        url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 15)))
        urls.append(f"http://{url}.com")
    return urls

def generate_random_date():
    year = random.randint(2010, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.datetime(year, month, day).strftime("%Y-%m-%d")


def generate_random_user(id):
    user = {
        "User_Id": id,
        "First_Name": f"User{id}",
        "Last_Name": f"LastName{id}",
        "Age": random.randint(18, 50)  # Random age between 18 and 50
    }
    return user

def generate_session_data(user_id, session_id):
    session = {
            "SessionId": session_id,
            "UserId": user_id,
            "SessionSearchAmount": random.randint(1, 10),
            "SessionLinkClicks": random.randint(1, 20),
            "SessionLifeTime": random.randint(100, 1000),  # Random session lifetime
            "SessionStartDate": generate_random_date(),
            "SessionLinks": generate_random_urls(5)  # Generate 5 random URLs for session links
    }
    return session

def generate_total_data(user_id):
    total_data = {
        "TotalId": user_id,
        "UserId": user_id,
        "TotalLinkClickAmount": random.randint(10, 100),
        "ListOfUrls": generate_random_urls(10)  # Generate 10 random URLs for total list of URLs
    }
    return total_data

# Generate random user data
def generate_data(num_users):
    all_users = []
    for i in range(0, num_users):
        user = generate_random_user(i)
        # Generate session user data for each user
        session_user_data = []
        for j in range(1, 6):  # Generate 5 sessions per user
            session_user_data.append(generate_session_data(i, j))

        total_data = generate_total_data(i)

        # Add session user data and total data to the user dictionary
        user["Session_User_Data"] = session_user_data
        user["Total_Data"] = total_data
        all_users.append(user)
    return all_users

# Save all data to a JSON file
with open("all_user_data_with_urls.json", "w") as json_file:
    json.dump(generate_data(100), json_file)

print("All user data with random URLs has been saved to 'all_user_data_with_urls.json'.")




## docker run --name mongo -d -p 27017:27017 mongodb/mongodb-community-server:7.0.5-ubuntu2204

#import json

### Load user data from the JSON file
# with open("users_data.json", "r") as json_file:
#  all_users = json.load(json_file)

### Now you can use the 'all_users' list containing user data in your code
