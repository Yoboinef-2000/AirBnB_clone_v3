#!/usr/bin/python3

from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieveAllStates():
    alltheStates = storage.all(State).values()
    alltheStatesList = []
    for aState in alltheStates:
        alltheStatesList.append(aState.to_dict())
    return jsonify(alltheStatesList)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getState(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    if not request.json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    if 'name' not in request.json:
        errorMsg = "Missing name"
        abort(400, description=errorMsg)
    data = request.json
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.json
    ignoreTheseKeys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
