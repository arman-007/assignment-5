import uuid
from .dummy_data import destinations


def get_all_destinations():
    return destinations # Return the list of destinations

def add_new_destination(data):
    new_destination = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'description': data['description'],
        'location': data['location'],
    }
    destinations.append(new_destination)
    return new_destination, 201

def delete_destination(id):
    destination = next((dest for dest in destinations if dest['id'] == id), None)
    if destination:
        destinations.remove(destination)
        return {'message': 'Destination deleted successfully'}, 200
    else:
        return {'message': 'Destination not found'}, 404