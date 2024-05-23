import time
from tabulate import tabulate
from Redis.RedisCache import MyRedisClientFactory



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
    client = MyRedisClientFactory.create_client()
    client.connect()
    
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    userId = "some_user_id"
    sessionId = "some_session_id"

    query_results_lifetime = measure_query_performance(client.get_lifetimeByDate_cache, start_date, end_date)
    query_results_session = measure_query_performance(client.getSessionSpecificWithUser_cache, userId, sessionId)

    headers = ["Name", "Avg (ms)", "Min (ms)", "Max (ms)", "10% (ms)", "50% (ms)", "90% (ms)", "QPS (queries/s)"]
    table = [
        ["getLifetimeByDate"] + list(query_results_lifetime.values()),
        ["getSessionSpecificWithUser"] + list(query_results_session.values())
    ]

    print(tabulate(table, headers, tablefmt="grid"))

        