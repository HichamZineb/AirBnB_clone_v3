#!/usr/bin/python3
"""
This module handles all default RESTFul API actions
for the link between Place and Amenity """

from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_places_amenities(place_id):
    """ Retrieves the list of all amenities for a given place id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])

    return jsonify([storage.get(Amenity, id).to_dict()
                    for id in place.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """ Deletes an Amenity by id """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """ Links an Amenity to a Place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return (jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return (jsonify(amenity.to_dict()), 201)
