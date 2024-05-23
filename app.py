import argparse
import Controllers.AnalyticsEndpoints as ae
import Mongo.ContextBuild as CtxBld
import Redis.RedisTabulate as redisTabulate
import Mongo.MyMongoTabulate as mongoTabulate

from flask import Flask
from flask_cors import CORS

# Create the Flask app and configure it
app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

# Create an instance of AnalyticsEndpoints and register endpoints
analytics_endpoints = ae.AnalyticsEndpoints()
analytics_endpoints.register_endpoints()

# Use the endPoint blueprint object for registration
app.register_blueprint(ae.endPoint)

# Function to parse command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("--redis_test", action="store_true", help="Perform Redis operations (testing)")
parser.add_argument("--mongo_test", action="store_true", help="Perform MongoDB operations (testing)")
parser.add_argument("--rebuildDb", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--norun", action="store_true", help="Perform all operations (testing)")

args = parser.parse_args()

if args.redis_test:
    print("Testing Redis operations...")
    try:
        redisTabulate.main()  # Call Redis functionality using try-except for error handling
    except Exception as e:
        print(f"Error during Redis operations: {e}")


if args.rebuildDb:
    print("Rebuilding MongoDB database...")
    try:
        CtxBld.ContextBuild.rebuildDb()
        
    except Exception as e:
        print(f"Error during MongoDB operations: {e}")

if args.mongo_test:
    print("Testing MongoDB operations..." )
    try:
        mongoTabulate.main()
    except Exception as e:
        print(f"Error during MongoDB operations: {e}")
        
if __name__ == "__main__" and not args.norun:
    app.run(host="0.0.0.0", port=8080)
