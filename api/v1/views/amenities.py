#!/usr/bin/python3
"""
This module handles all default RESTFul API actions for Amenity object
"""

from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity).values()
    amenities_json = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves Amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())

    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object by its id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return (jsonify({}), 200)

    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity """
    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    if "name" not in JSON_data:
        abort(400, "Missing name")

    valid_amenity = Amenity(**JSON_data)
    storage.new(valid_amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object by its id
    """
    amenityToUpdate = storage.get(Amenity, amenity_id)
    if amenityToUpdate is None:
        abort(404)

    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in JSON_data.items():
        if key not in ignored_keys:
            setattr(amenityToUpdate, key, value)
    storage.save()
    return (jsonify(amenityToUpdate.to_dict()), 200)
