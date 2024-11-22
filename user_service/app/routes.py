from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import ValidationError
import requests
import os
from dotenv import load_dotenv

from .utils import token_required
from .models import UserRegistrationModel, UserLoginModel

load_dotenv()

AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')

# Create a blueprint for user routes
user_bp = Blueprint('user_bp', __name__)

# Add security definitions
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add "Bearer " followed by your token'
    }
}
api = Api(version='1.0', title='User API', description='API for user registration and management', authorizations=authorizations, security='Bearer Auth')

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
        try:
            data = UserRegistrationModel(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400
        email = data.email
        if email in users:
            return {'error': 'User already exists'}, 400

        hashed_password = generate_password_hash(data.password, method='pbkdf2:sha256')
        users[email] = data.dict()
        users[email]['password'] = hashed_password

        return {'message': 'User successfully registered'}, 201

# Endpoint to authenticate a user
@user_ns.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid email or password')
    def post(self):
        try:
            data = UserLoginModel(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400

        user = users.get(data.email)
        if user and check_password_hash(user['password'], data.password):
            # Authentication logic here
            return {'message': 'Login successful'}, 200
        else:
            return {'error': 'Invalid email or password'}, 401


# Endpoint to get profile information
@user_ns.route('/profile')
class Profile(Resource):
    # @api.doc(params={'Authorization': {'in': 'header', 'description': 'Bearer token'}})
    @api.response(200, 'User profile retrieved')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    @token_required
    def get(self):
        # print(users)
        email = request.user['email']
        # print(request.headers.get('Authorization'))
        user = users.get(email)

        if user:
            return {
                'name': user['name'], 
                'email': user['email'], 
                'role': user['role']
            }, 200
        else:
            return {'error': 'User not found'}, 404
