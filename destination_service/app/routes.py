from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, Namespace


from .models import destinations  # Import destinations from models.py


# Create an API and a namespace for destination routes
api = Api(
    title='Destination Service API',
    version='1.0',
    description='API for managing travel destinations'
)

destination_ns = Namespace('destinations', description='Destination operations')

# Add the namespace to the API
api.add_namespace(destination_ns)


# Create a blueprint for destination routes
destination_bp = Blueprint('destination_bp', __name__)


# Endpoint to get all destinations
@destination_bp.route('/destinations', methods=['GET'])
def get_destinations():
    return jsonify(destinations), 200


# Endpoint to delete a destination (Admin-only)
@destination_bp.route('/destinations/<int:id>', methods=['DELETE'])
def delete_destination(id):
    # Assuming some role-based check here for admin access
    destination = next(
        (dest for dest in destinations if dest['id'] == id), None)
    if destination:
        destinations.remove(destination)
        return jsonify({'message': 'Destination deleted successfully'}), 200
    else:
        return jsonify({'error': 'Destination not found'}), 404
