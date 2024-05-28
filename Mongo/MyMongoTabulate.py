import time
from tabulate import tabulate
from Mongo.MyMongoClient import MyMongoFactory
from DataCreation import generate_data


# Function to measure query performance
def measure_query_performance(query_function, iterations, list=[], *args):
    try:
        times = []
        total_start_time = time.time()
        if len(list) > 0:
            # When adding users we need to be mindful of the unique id therefore we iterate over a list instead of calling with the exact same args
            for item in list:
                start_time = time.time()
                query_function(item)
                end_time = time.time()
                times.append((end_time - start_time) * 1000)
        else:
            for _ in range(iterations):
                start_time = time.time()
                query_function(*args)
                end_time = time.time()
                times.append((end_time - start_time) * 1000)
        total_end_time = time.time()

        times.sort()
        avg_time = sum(times) / len(times)
        min_time = times[0]
        max_time = times[-1]
        p10_time = times[int(0.1 * len(times))]
        p50_time = times[int(0.5 * len(times))]
        p90_time = times[int(0.9 * len(times))]
        qps = 1000 / avg_time if avg_time > 0 else 0
        total_time = total_end_time - total_start_time

        return {
            "Avg (ms)": avg_time,
            "Min (ms)": min_time,
            "Max (ms)": max_time,
            "10% (ms)": p10_time,
            "50% (ms)": p50_time,
            "90% (ms)": p90_time,
            "QPS (queries/s)": qps,
            "Total Time": total_time,
            "Total Queries": iterations
        }
    except Exception as e:
        print(f"Error in querying: {e}")


# Main function to execute the benchmark
def main(dbName):
    try:
        print(f"Running benchmark for MongoDB database '{dbName}' without cache...")
        
        client = MyMongoFactory.create_client(dbName)
        client.connect()

        iterations = 1000
        start_date = "2020-01-01"
        end_date = "2021-12-31"
        sessionId = 1
        
    
        user_data = generate_data(iterations)
        url = user_data[iterations % 2]["Total_Data"]["ListOfUrls"][0]
        userId = user_data[iterations % 2]["User_Id"]
        
        # CREATE USERS FIRST
        query_result_insert = measure_query_performance(client.create_user, iterations, user_data)
        
        # THEN MAKE OTHER QUERIES
        query_result_website = measure_query_performance(client.get_users_by_website, iterations, [], url)
        query_results_lifetime = measure_query_performance(client.getLifetimeByDate, iterations, [], start_date, end_date)
        query_results_session = measure_query_performance(client.getSessionSpecificWithUser, iterations, [], userId, sessionId)

        headers = ["Name", "Avg (ms)", "Min (ms)", "Max (ms)", "10% (ms)", "50% (ms)", "90% (ms)", "QPS (queries/s)", "Total Time", "Total Queries"]
        table = [
            ["Create_User"] + list(query_result_insert.values()),
            ["get_Users_By_Website"] + list(query_result_website.values()),
            ["get_Lifetime_By_Date"] + list(query_results_lifetime.values()),
            ["get_Session_Specific_By_User"] + list(query_results_session.values()),
        ]
    except Exception as e:
        print(f"Error in tabulation: {e}")
    finally:
        try:
            # Remove test users
            client.remove_test_users(user_data)
        except Exception as e:
            print(f"Error in removal: {e}")

    print(tabulate(table, headers, tablefmt="grid"))
