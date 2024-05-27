#!/usr/bin/python3

from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def cityPlaces(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    allthePlaces = []
    for aPlace in city.places:
        allthePlaces.append(aPlace.to_dict())
    return jsonify(allthePlaces)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletePlace(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def createPlace(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    if 'user_id' not in data:
        errorMsg = "Missing user_id"
        abort(400, description=errorMsg)
    user_id = data['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    if 'name' not in data:
        errorMsg = "Missing name"
        abort(400, description=errorMsg)
    place = Place(city_id=city_id, **data)
    place.save()
    return jsonify(place.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    ignoreTheseKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
