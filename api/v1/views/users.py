#!/usr/bin/python3

"""
Provide RESTful API actions for User objects.
User objects may rest now.
"""

from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieveAllTheUsers():
    users = storage.all(User).values()
    alltheUsers = []
    for aUser in users:
        alltheUsers.append(aUser.to_dict())
    return jsonify(alltheUsers)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getUser(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    if 'email' not in data:
        errorMsg = "Missing email"
        abort(400, description=errorMsg)
    if 'password' not in data:
        errorMsg = "Missing password"
        abort(400, description=errorMsg)
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    ignoreTheseKeys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
