from flask import Blueprint, request, jsonify
import jwt
import datetime

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Secret key for signing JWT tokens (normally, keep this secret and in environment variables)
SECRET_KEY = "your_secret_key"

# Endpoint to generate a token
@auth_bp.route('/auth/token', methods=['POST'])
def generate_token():
    data = request.get_json()
    email = data.get('email')
    role = data.get('role')

    if not email or not role:
        return jsonify({'error': 'Email and role are required'}), 400

    # Create a token valid for 1 hour
    token = jwt.encode({'email': email, 'role': role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token}), 200

# Middleware-like endpoint to validate the token (mock implementation)
@auth_bp.route('/auth/validate', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token is missing'}), 403

    try:
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'email': data['email'], 'role': data['role']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
