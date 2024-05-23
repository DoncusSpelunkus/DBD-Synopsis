from pymongo import MongoClient
from tabulate import tabulate
import time

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
        session_data = db.get_collection("Session_User").find({},{"_id": 0})
        result = []
        if session_data:
            for session in session_data:
                result.append(session)
        else:
            print("No users found between 18 and 21 years old in the specified date range.")
        
        return list(result)
    
    
# Function to measure query performance
def measure_query_performance(query_function, *args, iterations=10):
    times = []
    for _ in range(iterations):
        start_time = time.time()
        query_function(*args)
        end_time = time.time()
        times.append((end_time - start_time) * 1000)  # Convert to milliseconds

    times.sort()
    avg_time = sum(times) / len(times)
    min_time = times[0]
    max_time = times[-1]
    p10_time = times[int(0.1 * len(times))]
    p50_time = times[int(0.5 * len(times))]
    p90_time = times[int(0.9 * len(times))]
    qps = 1000 / avg_time if avg_time > 0 else 0

    return {
        "Avg (ms)": avg_time,
        "Min (ms)": min_time,
        "Max (ms)": max_time,
        "10% (ms)": p10_time,
        "50% (ms)": p50_time,
        "90% (ms)": p90_time,
        "QPS (queries/s)": qps
    }

# Main function to execute the benchmark
def main():
    client = MyMongoFactory.create_client()
    client.connect()
    
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    userId = "some_user_id"
    sessionId = "some_session_id"

    query_results_lifetime = measure_query_performance(client.getLifetimeByDate, start_date, end_date)
    query_results_session = measure_query_performance(client.getSessionSpecificWithUser, userId, sessionId)

    headers = ["Name", "Avg (ms)", "Min (ms)", "Max (ms)", "10% (ms)", "50% (ms)", "90% (ms)", "QPS (queries/s)"]
    table = [
        ["getLifetimeByDate"] + list(query_results_lifetime.values()),
        ["getSessionSpecificWithUser"] + list(query_results_session.values())
    ]

    print(tabulate(table, headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
