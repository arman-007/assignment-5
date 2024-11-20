from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Create a blueprint for user routes
user_bp = Blueprint('user_bp', __name__)

# In-memory storage for users
users = {}

# Endpoint to register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    if email in users:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(data.get('password'), method='sha256')
    users[email] = {
        'name': data.get('name'),
        'email': email,
        'password': hashed_password,
        'role': data.get('role', 'User')  # Default role is 'User'
    }

    return jsonify({'message': 'User registered successfully'}), 201

# Endpoint to authenticate a user
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users.get(email)
    if user and check_password_hash(user['password'], password):
        # In a real application, you'd return a JWT or other token
        return jsonify({'message': 'Login successful', 'role': user['role']}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Endpoint to get profile information
@user_bp.route('/profile', methods=['GET'])
def profile():
    # Assume this is done after authentication and token validation
    email = request.headers.get('email')  # For simplicity, using email header
    user = users.get(email)

    if user:
        return jsonify({'name': user['name'], 'email': user['email'], 'role': user['role']}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
