import redis
import Mongo.MyMongoClient as mongo
import json
import datetime as dt
from tabulate import tabulate
import time

class MyRedisClientFactory:
    @staticmethod
    def create_client():
        return MyRedisClient("localhost", 6379, "")
    
    
class MyRedisClient:
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password
        self.mongoClient = mongo.MyMongoFactory.create_client()
        self.redis_client = None  # Initialize redis_client as None
        self.mongoClient.connect()
        

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
        return self.redis_client
        
    
    def get_lifetimeByDate_cache(self, start_date, end_date):
        expiration_time = 1
        cachedKey = "from" + start_date + "to" + end_date
        db = self.getDb()
        
        if db.exists(cachedKey):
            return json.loads(db.get(cachedKey))
        else:
            result = self.mongoClient.getLifetimeByDate(start_date, end_date)
            db.set(cachedKey, json.dumps(result), ex=expiration_time)
    
    
    def getSessionSpecificWithUser_cache(self, userId, sessionId):
        expiration_time = 1
        cachedKey = f"userId:{userId}:sessionId:{sessionId}"
        db = self.getDb()
        
        if db.exists(cachedKey):
            print("Cache hit")
            return json.loads(db.get(cachedKey))
        else:
            result = self.mongoClient.getSessionSpecificWithUser(userId, sessionId)
            db.set(cachedKey, json.dumps(result), ex=expiration_time)
            
    
    def getAllSessions_cache(self):
        expiration_time = 1
        cachedKey = "allSessions"
        db = self.getDb()
        
        if db.exists(cachedKey):
            print("Cache hit")
            return json.loads(db.get(cachedKey))
        else:
            result = self.mongoClient.getAllSessions()
            db.set(cachedKey, json.dumps(result), ex=expiration_time)
            
    def getSortedSessions_cache(self, start_date, end_date):
        expiration_time = 60
        cachedKey = "newlist2"
        db = self.getDb()
        
        result = []
        
        if db.exists(cachedKey):
            start_date_epoch = int(dt.datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
            end_date_epoch = int(dt.datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
            print("Cache hit")
            sorted_sessions = db.zrangebyscore(cachedKey, min=start_date_epoch, max=end_date_epoch)
            for session in sorted_sessions:
                result.append(json.loads(session))
        else:
            result = self.mongoClient.getAllSessions()
            for document in result:
                print(document)
                score = int(dt.datetime.strptime(document["SessionStartDate"],"%Y-%m-%d").timestamp() * 1000)
                print(score)
                json_document = json.dumps(document) 
                db.zadd(cachedKey, {json_document: score})
            
        return result
    
