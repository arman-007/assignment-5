from functools import wraps
from flask import request, jsonify

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        # Extract and verify token (pseudocode)
        data = verify_token(token)
        if not data or data['role'] != 'Admin':
            return jsonify({'message': 'Admin access required'}), 403

        return f(*args, **kwargs)
    
    return decorated_function
