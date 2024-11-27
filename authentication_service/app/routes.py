from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
import jwt as pyjwt
import os
import datetime

from .utils import verify_token

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)
api = Api(version='1.0', title='Auth API', description='API for authentication and token management')
# Namespace for user operations
auth_ns = Namespace('authentication', description='Authentication operations')
api.add_namespace(auth_ns)

# Secret key for signing JWT tokens (normally, keep this secret and in environment variables)
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

# Define the user model for Swagger documentation
user_model = api.model('User', {
    'email': fields.String(required=True, description='The user\'s email'),
    'role': fields.String(required=True, description='The user\'s role')
})

# Define the token model for Swagger documentation
token_model = api.model('Token', {
    'token': fields.String(required=True, description='JWT token')
})

# Endpoint to generate a token
@api.route('/auth/token')
class GenerateToken(Resource):
    @api.expect(user_model)
    @api.response(200, 'Token generated successfully', token_model)
    @api.response(400, 'Email and role are required')
    def post(self):
        data = request.get_json()
        email = data.get('email')
        role = data.get('role')

        if not email or not role:
            return {'error': 'Email and role are required'}, 400

        # Create a token valid for 1 hour
        token = pyjwt.encode({'email': email, 'role': role, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
        # print("received token in /auth/token: ", token)
        return {'token': token}, 200
    

# Middleware-like endpoint to validate the token (mock implementation)
@api.route('/auth/validate')
class ValidateToken(Resource):
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'Bearer token'}})
    @api.response(200, 'Token is valid')
    @api.response(401, 'Invalid token')
    @api.response(403, 'Token is missing')
    def post(self):
        auth_header = request.headers.get('Authorization')

        print("auth_header in /validate", auth_header)
        if not auth_header:
            return {'error': 'Token is missing'}, 403

        # Strip the "Bearer" prefix if present
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header

        data = verify_token(token)
        if 'error' in data:
            return data, 401

        return {'email': data['email'], 'role': data['role']}, 200