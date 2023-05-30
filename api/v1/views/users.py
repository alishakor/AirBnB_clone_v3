#!/usr/bin/python3
"""This module defines a view for User objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects or creates a new one"""
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """Retrieves, deletes or updates a User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
