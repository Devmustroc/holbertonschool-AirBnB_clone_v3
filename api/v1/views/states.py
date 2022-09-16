#!/usr/bin/python3

from flask import jsonify, abort, request

from models import storage


def getstate(state):
    """Get state"""
    if not state:
        abort(404)
    return (jsonify(state.to_dict()), 200)


def pustate(state):
    """update state"""
    if not state:
        abort(404)
    if not request.is_json():
        abort(404, "Not a JSON")
    new_req = request.get_json()
    for (ks, val) in new_req.items():
        if ks != "id" and ks != "updated_at" and ks != "created_at":
            setattr(state, ks, val)
    storage.save()
    return jsonify(state.to_dict(), 200)
