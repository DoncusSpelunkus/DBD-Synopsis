import RedisCache as cache
from flask import jsonify, request, Blueprint

endPoint = Blueprint("main", __name__)

class AnalyticsEndpoints:
    def __init__(self):
        self.redis_client = cache.MyRedisClientFactory.create_client()
        self.redis_client.connect()
    
    def register_endpoints(self):
        # Register each endpoint individually
        endPoint.add_url_rule("/getLifetimeByDate", methods=["POST"], view_func=self.getLifetimeByDate)
        # Add more endpoints similarly
        
    def getLifetimeByDate(self):
        start_date = request.json["startDate"]
        end_date = request.json["endDate"]
        result = self.redis_client.get_lifetimeByDate_cache(start_date, end_date)
        return jsonify(result)