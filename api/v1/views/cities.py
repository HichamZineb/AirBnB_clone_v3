#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_by_state(state_id):
    '''Retrieves a list of all City objects'''
    States = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in States if obj.id == state_id]
    if state_obj == []:
        abort(404)
    Cities = [obj.to_dict() for obj in storage.all("City").values()
              if state_id == obj.state_id]
    return jsonify(Cities)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    States = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in States if obj.id == state_id]
    if state_obj == []:
        abort(404)
    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''Retrieves a City object'''
    Cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in Cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    return jsonify(city_obj[0])


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''Deletes a City object'''
    Cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in Cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    city_obj.remove(city_obj[0])
    for obj in Cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updates_city(city_id):
    '''Updates a City object'''
    Cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in Cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_obj[0]['name'] = request.json['name']
    for obj in Cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city_obj[0]), 200
