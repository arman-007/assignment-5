from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')

# Create a blueprint for user routes
user_bp = Blueprint('user_bp', __name__)
api = Api(version='1.0', title='User API', description='API for user registration and management')

# In-memory storage for users
users = {}

# Define the user model for Swagger documentation
user_model = api.model('User', {
    'name': fields.String(required=True, description='The user\'s name'),
    'email': fields.String(required=True, description='The user\'s email'),
    'password': fields.String(required=True, description='The user\'s password'),
    'role': fields.String(required=True, description='The user\'s role', enum=['Admin', 'User'])
})
login_model = api.model('Login', {
    'email': fields.String(required=True, description='The user\'s email'),
    'password': fields.String(required=True, description='The user\'s password'),
})

# Namespace for user operations
user_ns = Namespace('Users', description='User operations')
api.add_namespace(user_ns)

# Endpoint to register a new user
@user_ns.route('/register')
class Register(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully registered')
    @api.response(400, 'Invalid email or password')
    def post(self):
        data = request.get_json()
        email = data.get('email')
        if email in users:
            return {'error': 'User already exists'}, 400

        hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256')
        users[email] = {
            'name': data.get('name'),
            'email': email,
            'password': hashed_password,
            'role': data.get('role')
        }
        # print(users)
        return {'message': 'User successfully registered'}, 201

# Endpoint to authenticate a user
@user_ns.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid email or password')
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            print(f'{AUTHENTICATION_SERVICE_URL}/auth/token')
            return {'message': 'Login successful'}, 200
            # response = requests.post(f'{AUTHENTICATION_SERVICE_URL}/auth/token', json={'email': email, 'role': user['role']})
            # if response.status_code == 200:
            #     return response.json(), 200
            # else:
            #     return response.json(), response.status_code
        else:
            return {'error': 'Invalid email or password'}, 401


# Endpoint to get profile information
@user_ns.route('/profile')
class Profile(Resource):
    @api.doc(params={'email': {'in': 'header', 'description': 'The user\'s email'}})
    @api.response(200, 'User profile retrieved')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'User not found')
    def get(self):
        print(users)
        email = request.headers.get('email')
        user = users.get(email)

        if user:
            return {'name': user['name'], 'email': user['email'], 'role': user['role']}, 200
        else:
            return {'error': 'User not found'}, 404
