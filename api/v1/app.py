#!/usr/bin/python3
"""starts a Flask web application"""
from os import getenv

from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exec):
    """call storage and close it"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle error function"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
