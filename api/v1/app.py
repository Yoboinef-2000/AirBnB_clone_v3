#!/usr/bin/python3

from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearItAllUp(error):
    storage.close()


@app.errorhandler(404)
def weNotHereBabyWeOut(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # host = getenv('HBNB_API_HOST', '0.0.0.0')
    # Just for Clarificcation,
    # host will try to retrieve the env variabble
    # named HBNB_API_HOST, but if that env var is not
    # set, it will default to the 0.0.0.0 IP

    # The same thing applies for port too

    # Now that that's out of the way,
    # Ask your self this:
    # A hundred shots, a hundred shots, how you miss a whole 100 shots?
    # Lol
    # port = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, threaded=True)
    # host=host, port=port,
