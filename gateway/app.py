from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import requests 
import os


from destination_service.app.routes import destination_bp  # Import the blueprint

app = Flask(__name__)

api = Api(
    app,
    title='Travel API Gateway',
    version='1.0',
    description='API Gateway for managing travel services'
)

# Register the blueprint
app.register_blueprint(destination_bp)

# Define the base URLs for each microservice
DESTINATION_SERVICE_URL = os.getenv('DESTINATION_SERVICE_URL')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')



@api.route('/')
class Welcome(Resource):
    def get(self):
        """Welcome message to ensure server is running"""
        return {'message': 'Welcome to the Travel API Gateway! The server is running.'}, 200

# Route for Destinations (Forwarding request to Destination Service)
@app.route('/destinations', methods=['GET', 'DELETE'])
def destinations():
    if request.method == 'GET':
        """Get all destinations from Destination Service"""
        response = requests.get(f"{DESTINATION_SERVICE_URL}/destinations")
        return response.content, response.status_code

    elif request.method == 'DELETE':
        """Delete a specific destination (Admin only)"""
        destination_id = request.args.get('id')
        response = requests.delete(f"{DESTINATION_SERVICE_URL}/destinations/{destination_id}", headers=request.headers)
        return response.content, response.status_code

# Route for User Registration and Login (Forwarding request to User Service)
@api.route('/register')
class RegisterUser(Resource):
    def post(self):
        """Register a new user via User Service"""
        response = requests.post(f"{USER_SERVICE_URL}/register", json=request.get_json())
        return (response.content, response.status_code)

@api.route('/login')
class LoginUser(Resource):
    def post(self):
        """Login user via User Service"""
        response = requests.post(f"{USER_SERVICE_URL}/login", json=request.get_json())
        return (response.content, response.status_code)

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
