#!/usr/bin/python3

from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models import state


def getstate(state):
    """Get state"""
    if not state:
        abort(404)
    return (jsonify(state.to_dict()), 200)


def update_state(state):
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


def state_delete(state):
    """delete state"""
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


app_views.route("/states", methods=["GET", "POST"])


def states():
    """Retrieves list of all state objs or creates a state"""
    if request.method == "GET":
        all_states = [st.to_dict() for st in storage.all('state').values()]
        return (jsonify(all_states), 200)
    elif request.method == "POST":
        if not request.is_json:
            abort(400, "NOT a JSON")
        new_JSon = request.get_json()
        if 'name' not in new_JSon.keys():
            abort(400, "Missing name")
        sT = state()
        for (ks, val) in new_JSon.items():
            setattr(sT, ks, val)
        sT.save()
        return (jsonify(sT.to_dict(), 201)

@app_views.route("/states/<ident>", methods=["GET", "PUT", "DELETE"])


