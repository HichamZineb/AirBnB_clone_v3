#!/usr/bin/python3
"""
This module handles all default RESTFul API actions for Place object
"""

from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get(City, city_id)
    if city:
        places_json = [place.to_dict() for place in city.places]
        return jsonify(places_json)
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves Place object by its id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())

    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object by its id """
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return (jsonify({}), 200)

    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    if "name" not in JSON_data:
        abort(400, "Missing name")

    if "user_id" not in JSON_data:
        abort(400, "Missing user_id")

    user_id = JSON_data['user_id']
    user = storage.get(User, user_id)
    city = storage.get(City, city_id)
    if city is None or user is None:
        abort(404)

    valid_place = Place(**JSON_data)
    storage.new(valid_place)
    storage.save()
    return (jsonify(valid_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by its id
    """
    placeToUpdate = storage.get(Place, place_id)
    if placeToUpdate is None:
        abort(404)

    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in JSON_data.items():
        if key not in ignored_keys:
            setattr(placeToUpdate, key, value)
    storage.save()
    return (jsonify(placeToUpdate.to_dict()), 200)
