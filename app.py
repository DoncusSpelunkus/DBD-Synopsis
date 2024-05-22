from flask import Flask
from flask_cors import CORS
import AnalyticsEndpoints as ae

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

# Create an instance of AnalyticsEndpoints and register endpoints
analytics_endpoints = ae.AnalyticsEndpoints()
analytics_endpoints.register_endpoints()

# Use the endPoint blueprint object for registration
app.register_blueprint(ae.endPoint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)