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
parser.add_argument("--no_run", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--both", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--index", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--no_index", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--deleteDb", action="store_true", help="Perform all operations (testing)")
parser.add_argument("--test_all", action="store_true", help="Perform MongoDB operations (testing)")

args = parser.parse_args()


def mongo_tabulate(dbName):
    try:
        mongoTabulate.main(dbName)  # Call MongoDB functionality using try-except for error handling
    except Exception as e:
        print(f"Error during Mongo tabulation operations: {e}")

def redis_tabulate(dbName):
    try:
        redisTabulate.main(dbName)  # Call Redis functionality using try-except for error handling
    except Exception as e:
        print(f"Error during Redis tabulation operations: {e}")
        

## Argument parsing        
if args.redis_test:
    redis_tabulate("Index")  # Call Redis functionality using try-except for error handling
    

if args.rebuildDb:
    if args.both | args.index:
        print("Rebuilding indexed db...")
        CtxBld.ContextBuild.rebuildIndexedDb()
    if args.both | args.no_index:
        print("Rebuilding non-indexed db...")
        CtxBld.ContextBuild.rebuildNonIndexedDb()
    else:
        print("--rebuildDb requires --both or --index or --no_index to be set.")
        
if args.mongo_test:
    if args.both | args.index:
        mongo_tabulate("Index")
    if args.both | args.no_index:
        mongo_tabulate("NoIndex")
    else:
        print("--mongo_test requires --both or --index or --no_index to be set.")
        
if args.deleteDb:
    if args.both | args.index:
        print("Deleting indexed db...")
        CtxBld.ContextBuild.deleteDb("Index")
    if args.both | args.no_index:
        print("Deleting non-indexed db...")
        CtxBld.ContextBuild.deleteDb("NoIndex")
    else:
        print("--deleteDb requires --both or --index or --no_index to be set.")

if args.test_all:
    mongo_tabulate("Index")
    redis_tabulate("Index")
    mongo_tabulate("NoIndex")
    redis_tabulate("NoIndex")

if __name__ == "__main__" and not args.no_run:
    app.run(host="0.0.0.0", port=8080)
