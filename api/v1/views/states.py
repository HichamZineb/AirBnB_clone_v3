#!/usr/bin/python3
"""
This module handles all default RESTFul API actions for State object """

from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State).values()
    states_json = [state.to_dict() for state in all_states]
    return jsonify(states_json)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object by its id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())

    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object by its id """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return (jsonify({}), 200)

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    if "name" not in JSON_data:
        abort(400, "Missing name")

    valid_state = State(**JSON_data)
    storage.new(valid_state)
    storage.save()
    return (jsonify(valid_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its id
    """
    stateToUpdate = storage.get(State, state_id)
    if stateToUpdate is None:
        abort(404)

    JSON_data = request.get_json()
    if JSON_data is None:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in JSON_data.items():
        if key not in ignored_keys:
            setattr(stateToUpdate, key, value)
    storage.save()
    return (jsonify(stateToUpdate.to_dict()), 200)
