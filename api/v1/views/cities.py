#!/usr/bin/python3

"""
Provide RESTful API actions for City objects.
City objects may rest now.
"""

from flask import jsonify, abort, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def stateCities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    alltheCities = []
    for city in state.cities:
        alltheCities.append(city.to_dict())
    return jsonify(alltheCities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def createCity(state_id):
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if 'name' not in data:
        errorMsg = "Missing name"
        abort(400, description=errorMsg)
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    ignoreTheseKeys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
