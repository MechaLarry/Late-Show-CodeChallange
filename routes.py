from flask import Blueprint, jsonify, request, abort
from models import Episode, Guest, Appearance
from extensions import db  # Import db

# Define the blueprint for routes
api = Blueprint('api', __name__)

# Get all episodes
@api.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes]), 200

# Get a specific episode by ID
@api.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get_or_404(id)
    return jsonify(episode.to_dict()), 200

# Create a new episode
@api.route('/episodes', methods=['POST'])
def create_episode():
    data = request.get_json()
    
    if not data or 'title' not in data:
        abort(400, description="Missing required fields.")
    
    new_episode = Episode(
        title=data.get('title'),
        year=data.get('year'),
        air_date=data.get('air_date')
    )
    db.session.add(new_episode)
    db.session.commit()
    
    return jsonify(new_episode.to_dict()), 201

# Update an episode
@api.route('/episodes/<int:id>', methods=['PUT'])
def update_episode(id):
    episode = Episode.query.get_or_404(id)
    data = request.get_json()

    episode.title = data.get('title', episode.title)
    episode.year = data.get('year', episode.year)
    episode.air_date = data.get('air_date', episode.air_date)

    db.session.commit()

    return jsonify(episode.to_dict()), 200

# Delete an episode
@api.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get_or_404(id)
    db.session.delete(episode)
    db.session.commit()
    return '', 204

# Get all guests
@api.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests]), 200

# Get a specific guest by ID
@api.route('/guests/<int:id>', methods=['GET'])
def get_guest(id):
    guest = Guest.query.get_or_404(id)
    return jsonify(guest.to_dict()), 200

# Create a new guest
@api.route('/guests', methods=['POST'])
def create_guest():
    data = request.get_json()
    
    if not data or 'name' not in data:
        abort(400, description="Missing required fields.")
    
    new_guest = Guest(
        name=data.get('name'),
        occupation=data.get('occupation')
    )
    db.session.add(new_guest)
    db.session.commit()
    
    return jsonify(new_guest.to_dict()), 201

# Update a guest
@api.route('/guests/<int:id>', methods=['PUT'])
def update_guest(id):
    guest = Guest.query.get_or_404(id)
    data = request.get_json()

    guest.name = data.get('name', guest.name)
    guest.occupation = data.get('occupation', guest.occupation)

    db.session.commit()

    return jsonify(guest.to_dict()), 200

# Delete a guest
@api.route('/guests/<int:id>', methods=['DELETE'])
def delete_guest(id):
    guest = Guest.query.get_or_404(id)
    db.session.delete(guest)
    db.session.commit()
    return '', 204

# Get all appearances
@api.route('/appearances', methods=['GET'])
def get_appearances():
    appearances = Appearance.query.all()
    return jsonify([appearance.to_dict() for appearance in appearances]), 200

# Create a new appearance
@api.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    if not data or 'guest_id' not in data or 'episode_id' not in data:
        abort(400, description="Missing required fields.")
    
    new_appearance = Appearance(
        guest_id=data.get('guest_id'),
        episode_id=data.get('episode_id'),
        role=data.get('role')
    )
    db.session.add(new_appearance)
    db.session.commit()
    
    return jsonify(new_appearance.to_dict()), 201

# Delete an appearance
@api.route('/appearances/<int:id>', methods=['DELETE'])
def delete_appearance(id):
    appearance = Appearance.query.get_or_404(id)
    db.session.delete(appearance)
    db.session.commit()
    return '', 204
