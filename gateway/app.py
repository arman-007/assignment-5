from flask import Flask, request, jsonify, Response
from flask_restx import Api, Resource
from dotenv import load_dotenv
import requests
import sys
import os


from utils import proxy_request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

# from destination_service.app.routes import destination_bp
# from user_service.app.routes import user_bp
# from authentication_service.app.routes import auth_bp

app = Flask(__name__)

# api = Api(
#     app,
#     title='Travel API Gateway',
#     version='1.0',
#     description='API Gateway for managing travel services'
# )

# Register the blueprint
# app.register_blueprint(destination_bp, url_prefix='/api/destinations')
# app.register_blueprint(user_bp, url_prefix='/api/users')
# app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Define the base URLs for each microservice
DESTINATION_SERVICE_URL = os.getenv('DESTINATION_SERVICE_URL')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')

# print(f"Destination Service URL: {DESTINATION_SERVICE_URL}")
# print(f"User Service URL: {USER_SERVICE_URL}")
# print(f"Authentication Service URL: {AUTHENTICATION_SERVICE_URL}")


@app.route('/api/users/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_user_service(path):
    return proxy_request(USER_SERVICE_URL, path)

# Destination Service
@app.route('/api/destinations/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_destination_service(path):
    return proxy_request(DESTINATION_SERVICE_URL, path)

# Authentication Service
@app.route('/api/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_auth_service(path):
    return proxy_request(AUTHENTICATION_SERVICE_URL, path)

@app.route('/')
def index():
    return {'message': 'API Gateway is running'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
