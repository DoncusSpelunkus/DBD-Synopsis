import redis

class MyRedisClientFactory:
    @staticmethod
    def create_client():
        return MyRedisClient("localhost", 6379, "")
    
    
class MyRedisClient:
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password
        self.redis_client = None  # Initialize redis_client as None

    def __repr__(self):
        return f"MyRedisClient(host='{self.host}', port={self.port}, password='{self.password}')"
    
    def connect(self):
        print("trying to connect")
        try:
            self.redis_client = redis.Redis(host=self.host, port=self.port, password=self.password)
            # Test connection to see if it works
            if self.redis_client.ping():
                print(f"Connected to Redis at {self.host}:{self.port}")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")

    
    def getDb(self):
        self.redis_client.set("test", "test")
        result = self.redis_client.get("test")
        print(result)
        return self.redis_client
        
    
    def get_lifetimeByDate_cache(self, start_date, end_date):
        cache_key = f"sessionLifetime:{start_date}_to_{end_date}"
        db = self.getDb()
        
        cached_data = db.get(cache_key)
    