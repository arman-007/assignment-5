from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, Namespace, fields
from pydantic import ValidationError
import uuid

from .dummy_data import destinations  # Import destinations from models.py
from .utils import admin_required
from.models import NewDestinationModel
from .controllers import (
    get_all_destinations,
    add_new_destination, 
    delete_destination
)


# Create a blueprint for destination routes
destination_bp = Blueprint('destination_bp', __name__)

# Add security definitions
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add "Bearer " followed by your token'
    }
}
api = Api(version='1.0', title='Destination Service API', description='API for managing travel destinations', authorizations=authorizations, security='Bearer Auth')

# Namespace for destination operations
destination_ns = Namespace('destinations', description='Destination operations')
api.add_namespace(destination_ns)

# Define the new destination model for Swagger documentation
new_destination_model = api.model('NewDestination', {
    'name': fields.String(required=True, description='The destination name'),
    'description': fields.String(required=True, description='The destination description'),
    'location': fields.String(required=True, description='The destination location'),
})

# Class-based resource for getting all destinations
@destination_ns.route('/destinations')
class DestinationList(Resource):
    @destination_ns.doc('list_destinations')
    @destination_ns.response(200, 'Success')
    def get(self):
        """Get all destinations"""
        return get_all_destinations(), 200
    
# Class-based resource for adding a new destination
@destination_ns.route('/destination')
class AddDestination(Resource):
    @destination_ns.doc('add_destination')
    @destination_ns.expect(new_destination_model)
    @destination_ns.response(201, 'Destination added successfully')
    @destination_ns.response(400, 'Invalid input')
    @admin_required
    def post(self):
        """Add a new destination (Admin-only)"""
        try:
            data = NewDestinationModel(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400

        new_destination = data.model_dump()
        new_destination['id'] = str(uuid.uuid4())
        destinations.append(new_destination)

        return {'message': 'Destination added successfully'}, 201

# Class-based resource for deleting a destination
@destination_ns.route('/destinations/<int:id>')
class Destination(Resource):
    @destination_ns.doc('delete_destination')
    @destination_ns.response(200, 'Destination deleted successfully')
    @destination_ns.response(404, 'Destination not found')
    @admin_required
    
    def delete(self, id):
        """Delete a destination (Admin-only)"""
        return delete_destination(id)


