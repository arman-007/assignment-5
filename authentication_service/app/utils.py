import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY')

def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}