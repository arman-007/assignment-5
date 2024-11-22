from flask import request, jsonify
from functools import wraps
import os
import requests

AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')
if AUTHENTICATION_SERVICE_URL is None:
    raise ValueError("AUTHENTICATION_SERVICE_URL environment variable is not set")

# Token validation decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            print("token in token_required", token)
        if not token:
            return {'error': 'Token is missing'}, 401
        try:
            headers = {'Authorization': f'Bearer {token}'} #this is the token that is being sent to the authentication service
            response = requests.post(f'{AUTHENTICATION_SERVICE_URL}/auth/validate', headers=headers)
            if response.status_code != 200:
                print(response.json())
                return response.json(), response.status_code
            data = response.json()
            request.user = data
        except Exception as e:
            return {'error': 'Token is invalid'}, 401
        return f(*args, **kwargs)
    return decorated