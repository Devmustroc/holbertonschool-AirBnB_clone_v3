#!/usr/bin/python3
"""return JSON status on object app_views"""

from flask import jsonify

from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=["GET"])
def status():
    """Return /status api route"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Return status api route"""
    data = {
        "amenities": 47,
        "cities": 36,
        "places": 154,
        "reviews": 718,
        "states": 27,
        "users": 31
    }
    data = {ks: storage.count(val) for ks, val in data.items()}
    return jsonify(data)
