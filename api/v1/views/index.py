#!/usr/bin/python3
"""return JSON status on object app_views"""

from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=["GET"])
def status():
    """Return /status api route"""
    return jsonify({"status": "OK"})
