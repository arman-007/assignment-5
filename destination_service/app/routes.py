from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, Namespace
from .models import destinations  # Import destinations from models.py

# Create a blueprint for destination routes
destination_bp = Blueprint('destination_bp', __name__)
api = Api(version='1.0', title='Destination Service API', description='API for managing travel destinations')

# Namespace for destination operations
destination_ns = Namespace('destinations', description='Destination operations')
api.add_namespace(destination_ns)

# Class-based resource for getting all destinations
@destination_ns.route('/destinations')
class DestinationList(Resource):
    @destination_ns.doc('list_destinations')
    @destination_ns.response(200, 'Success')
    def get(self):
        """Get all destinations"""
        return destinations, 200

# Class-based resource for deleting a destination
@destination_ns.route('/destinations/<int:id>')
class Destination(Resource):
    @destination_ns.doc('delete_destination')
    @destination_ns.response(200, 'Destination deleted successfully')
    @destination_ns.response(404, 'Destination not found')
    def delete(self, id):
        """Delete a destination (Admin-only)"""
        destination = next((dest for dest in destinations if dest['id'] == id), None)
        
        if destination:
            destinations.remove(destination)
            return {'message': 'Destination deleted successfully'}, 200
        else:
            return {'message': 'Destination not found'}, 404


