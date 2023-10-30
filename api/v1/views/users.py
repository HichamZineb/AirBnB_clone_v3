#!/usr/bin/python3
"""users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''
    retrieves the list of all User objects
    '''
    # Get all User objects from the storage and convert them to dictionaries
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Retrieves a User object'''
    Users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in Users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a User object'''
    Users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in Users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for obj in Users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates a User'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')
    Users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    Users.append(new_user.to_dict())
    return jsonify(Users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    '''Updates a User object'''
    Users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in Users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_obj[0]['first_name'] = request.json['first_name']
    except Exception as e:
        pass
    try:
        user_obj[0]['last_name'] = request.json['last_name']
    except Exception as e:
        pass
    for obj in Users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except Exception as e:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except Exception as e:
                pass
    storage.save()
    return jsonify(user_obj[0]), 200
