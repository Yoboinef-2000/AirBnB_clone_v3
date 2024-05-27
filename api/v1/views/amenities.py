#!/usr/bin/python3

from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieveAllTheAmenities():
    amenities = storage.all(Amenity).values()
    allTheAmenities = []
    for anAmenity in amenities:
        allTheAmenities.append(anAmenity.to_dict())
    return jsonify(allTheAmenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def getAmenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteAmenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    if 'name' not in data:
        errorMsg = "Missing name"
        abort(400, description=errorMsg)
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def updateAmenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    ignoreTheseKeys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
