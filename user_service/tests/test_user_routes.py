import pytest
from flask import Flask
from user_service.app.routes import user_bp, api, users
from unittest.mock import patch
import os
from werkzeug.security import generate_password_hash
from flask import request
import requests_mock


AUTHENTICATION_SERVICE_URL = os.getenv('AUTHENTICATION_SERVICE_URL')

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    api.init_app(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_users():
    # Set up an initial user for testing
    global users
    users.clear()  # Clear users before each test to prevent conflicts
    users['test@example.com'] = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': generate_password_hash('password123', method='pbkdf2:sha256'),
        'role': 'User'
    }

# Test for user registration
def test_register_user_success(client):
    data = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'newpassword123',
        'role': 'User'
    }
    response = client.post('/users/register', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User successfully registered'

def test_register_user_already_exists(client, setup_users):
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'User'
    }
    response = client.post('/users/register', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'User already exists'

# Test for user login
def test_login_user_success(client, setup_users, requests_mock):
    # Mocking the authentication service
    requests_mock.post(f"{AUTHENTICATION_SERVICE_URL}/auth/token", json={'token': 'test_token'})

    data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = client.post('/users/login', json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'
    assert 'token' in response.get_json()

def test_login_user_invalid_credentials(client, setup_users):
    data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/users/login', json=data)
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid email or password'

# Test for retrieving user profile
def test_get_profile_success(client, setup_users, mocker):
    # Mock the token_required decorator to set the email in request context
    def mock_token_required(f):
        def decorated_function(*args, **kwargs):
            request.user = {'email': 'test@example.com'}
            return f(*args, **kwargs)
        return decorated_function

    mocker.patch('user_service.app.utils.token_required', mock_token_required)

    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFAYi5jb20iLCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3MzI0NzMzNDd9.sHt4DF565bgot8iN8sbvRWl-SU5xcLph4w21MDOfQUs'}
    response = client.get('/users/profile', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['email'] == 'test@example.com'

def test_get_profile_user_not_found(client, mocker):
    # Mock the token_required decorator to set a non-existing email
    def mock_token_required(f):
        def decorated_function(*args, **kwargs):
            request.user = {'email': 'nonexistent@example.com'}
            return f(*args, **kwargs)
        return decorated_function

    mocker.patch('user_service.app.utils.token_required', mock_token_required)

    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFAYi5jb20iLCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3MzI0NzMzNDd9.sHt4DF565bgot8iN8sbvRWl-SU5xcLph4w21MDOfQUs'}
    response = client.get('/users/profile', headers=headers)
    assert response.status_code == 404
    assert response.get_json()['error'] == 'User not found'
