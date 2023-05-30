#!/usr/bin/python3
"""This module defines a view for State objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects or creates a new one"""
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """Retrieves, deletes or updates a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
