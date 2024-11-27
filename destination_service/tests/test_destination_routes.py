import pytest
from flask import Flask
from destination_service.app.routes import destination_bp, api
from destination_service.app.dummy_data import destinations
from unittest.mock import patch
import os

TEST_TOKEN = os.getenv('TEST_TOKEN')

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(destination_bp)
    api.init_app(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def always_allow(f):
    return f

def test_get_all_destinations(client):
    response = client.get('/destinations/destinations')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_add_destination_success(client):
    headers = {'Authorization': f'Bearer {TEST_TOKEN}'}
    data = {
        'name': 'New Destination',
        'description': 'A beautiful place',
        'location': 'Wonderland'
    }
    with patch('destination_service.app.utils.admin_required', lambda f: f):  # Mocking admin_required decorator
        response = client.post('/destinations/destination', json=data, headers=headers)
        assert response.status_code == 201
        assert response.get_json()['message'] == 'Destination added successfully'
        assert any(dest['name'] == 'New Destination' for dest in destinations)

def test_add_destination_invalid_input(client):
    headers = {'Authorization': f'Bearer {TEST_TOKEN}'}
    data = {
        'name': 'Incomplete Destination'
        # Missing description and location
    }
    with patch('destination_service.app.utils.admin_required', lambda f: f):  # Mocking admin_required decorator
        response = client.post('/destinations/destination', json=data, headers=headers)
        assert response.status_code == 400
        assert 'errors' in response.get_json()

def test_delete_destination_success(client):
    headers = {'Authorization': f'Bearer {TEST_TOKEN}'}
    destination_id = destinations[0]['id']  # Assuming we have at least one destination
    with patch('destination_service.app.utils.admin_required', lambda f: f):  # Mocking admin_required decorator
        response = client.delete(f'/destinations/destinations/{destination_id}', headers=headers)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Destination deleted successfully'

def test_delete_destination_not_found(client):
    headers = {'Authorization': f'Bearer {TEST_TOKEN}'}
    with patch('destination_service.app.utils.admin_required', lambda f: f):  # Mocking admin_required decorator
        response = client.delete('/destinations/destinations/9999', headers=headers)
        assert response.status_code == 404
        assert response.get_json()['message'] == 'Destination not found'