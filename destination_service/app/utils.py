from functools import wraps
from flask import request, jsonify
import requests
import os


AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')
if AUTHENTICATION_SERVICE_URL is None:
    raise ValueError("AUTHENTICATION_SERVICE_URL environment variable is not set")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        print("token in admin_required", token)
        if not token:
            return {'message': 'Token is missing!'}, 403
        
        # Extract and verify token (pseudocode)
        try:
            headers = {'Authorization': token} #this is the token that is being sent to the authentication service
            response = requests.post(f'{AUTHENTICATION_SERVICE_URL}/auth/validate', headers=headers)
            if response.status_code != 200:
                print(response.json())
                return response.json(), response.status_code
            data = response.json()
            request.user = data
        except Exception as e:
            return {'error': 'Token is invalid'}, 401
        if not data or data['role'] != 'Admin':
            return {'message': 'You are not an admin. Admin access required'}, 403

        return f(*args, **kwargs)
    
    return decorated_function
