#!/usr/bin/python3
"""This module defines a view for City objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """
    Retrieves the list of all City objects of a State or creates a new one
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """Retrieves, deletes or updates a City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
