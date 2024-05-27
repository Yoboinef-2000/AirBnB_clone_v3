#!/usr/bin/python3

from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviewPlaces(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    allTheReviews = []
    for aReview in place.reviews:
        allTheReviews.append(aReview.to_dict())
    return jsonify(allTheReviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getReview(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteReview(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def createReview(place_id):
    place = storage.get(Place, place_id)
    if place is None:
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
    if 'text' not in data:
        errorMsg = "Missing text"
        abort(400, description=errorMsg)
    review = Review(place_id=place_id, **data)
    review.save()
    return jsonify(review.to_dict()), 201


# You said you wasnt with him
# Now you with him now huh?
# Things different now huh?
# You committed now huh?
# I guess I cant ........
# How I hit ........ now huh
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        errorMsg = "Not a JSON"
        abort(400, description=errorMsg)
    data = request.get_json()
    ignoreTheseKeys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignoreTheseKeys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
