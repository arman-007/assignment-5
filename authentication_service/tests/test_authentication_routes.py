import pytest
from flask import Flask
from authentication_service.app.routes import auth_bp, api
from unittest.mock import patch
import jwt as pyjwt
import os
import datetime

TEST_SECRET_KEY = '80ad6885d759269f38e7b2c2ea5aebcfe5c6c58577c3cfca177ec9d682262c63ae36e2de524eb63add6782b2d28ff412d99d4f810d3aa2e1f7b7b92d5ce4072d'

# Fixtures
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = TEST_SECRET_KEY
    os.environ['SECRET_KEY'] = TEST_SECRET_KEY
    app.register_blueprint(auth_bp)
    api.init_app(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test for token generation
def test_generate_token_success(client):
    data = {
        'email': 'testuser@example.com',
        'role': 'Admin'
    }
    response = client.post('/auth/token', json=data)
    assert response.status_code == 200
    assert 'token' in response.get_json()
    token = response.get_json()['token']

    # Decode the token to ensure it has correct data
    decoded_data = pyjwt.decode(token, TEST_SECRET_KEY, algorithms=['HS256'])
    assert decoded_data['email'] == data['email']
    assert decoded_data['role'] == data['role']

def test_generate_token_missing_fields(client):
    # Missing role
    data = {
        'email': 'testuser@example.com'
    }
    response = client.post('/auth/token', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Email and role are required'

# Test for token validation
def test_validate_token_success(client, mocker):
    # Create a valid token
    payload = {
        'email': 'testuser@example.com',
        'role': 'Admin',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = pyjwt.encode(payload, TEST_SECRET_KEY, algorithm='HS256')

    # Mock the verify_token function to avoid actual token decoding in the middleware
    mocker.patch('authentication_service.app.utils.verify_token', return_value=payload)

    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/auth/validate', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['email'] == payload['email']
    assert response.get_json()['role'] == payload['role']

def test_validate_token_missing_token(client):
    response = client.post('/auth/validate')
    assert response.status_code == 403
    assert response.get_json()['error'] == 'Token is missing'

def test_validate_token_invalid(client, mocker):
    # Mock the verify_token function to return an error for invalid token
    mocker.patch('authentication_service.app.utils.verify_token', return_value={'error': 'Invalid token'})

    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.post('/auth/validate', headers=headers)
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid token'
