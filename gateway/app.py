from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import requests 

app = Flask(__name__)

api = Api(
    app,
    title='Travel API Gateway',
    version='1.0',
    description='API Gateway for managing travel services'
)

# Define the base URLs for each microservice
DESTINATION_SERVICE_URL = 'http://127.0.0.1:5001'
USER_SERVICE_URL = 'http://127.0.0.1:5002'
AUTHENTICATION_SERVICE_URL = 'http://127.0.0.1:5003'



# Welcome endpoint to check if the server is running
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'message': 'Welcome to the Travel API Gateway! The server is running.'}), 200

# Route for Destinations (Forwarding request to Destination Service)
@app.route('/destinations', methods=['GET', 'DELETE'])
def destinations():
    if request.method == 'GET':
        response = requests.get(f"{DESTINATION_SERVICE_URL}/destinations")
    elif request.method == 'DELETE':
        destination_id = request.args.get('id')
        response = requests.delete(f"{DESTINATION_SERVICE_URL}/destinations/{destination_id}", headers=request.headers)
    
    return (response.content, response.status_code, response.headers.items())

# Route for User Registration and Login (Forwarding request to User Service)
@app.route('/register', methods=['POST'])
def register():
    response = requests.post(f"{USER_SERVICE_URL}/register", json=request.get_json())
    return (response.content, response.status_code, response.headers.items())

@app.route('/login', methods=['POST'])
def login():
    response = requests.post(f"{USER_SERVICE_URL}/login", json=request.get_json())
    return (response.content, response.status_code, response.headers.items())

@app.route('/profile', methods=['GET'])
def profile():
    response = requests.get(f"{USER_SERVICE_URL}/profile", headers=request.headers)
    return (response.content, response.status_code, response.headers.items())

# Authentication Service: Token management (e.g., role validation)
@app.route('/auth/token', methods=['POST'])
def auth_token():
    response = requests.post(f"{AUTHENTICATION_SERVICE_URL}/auth/token", json=request.get_json())
    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
