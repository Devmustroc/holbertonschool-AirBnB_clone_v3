#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage


def getstate(state):
    """Get state"""
    if not state:
        abort(404)
    return (jsonify(state.to_dict(), 200)



