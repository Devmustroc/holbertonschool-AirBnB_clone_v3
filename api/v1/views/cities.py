#!/usr/bin/python3
"""
Creates a new view for cities & all API actions
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City


def get_city(city):
    """get City Object"""
    return (city.to_dict(), 200)


def putcity(city):
    """Update City Object"""
    if not request.is_json:
        abort(404, "Not a JSON")
    new = request.get_json()
    for (ks, val) in new.items():
        if ks != "id" and ks != "created_at" and ks != "updated_at":
            setattr(city, ks, val)
    storage.save()
    return (city.to_dict(), 200)


def deletecity(city):
    """Delete City object"""
    storage.delete(city)
    storage.save()
    return ({}, 200)


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities(state_id):
    """Retrieves list of all objects"""
    state = None
    for sT in storage.all('state').value():
        if sT.id == state_id:
            state = sT
    if state is None:
        abort(400)
    if request.method == "GET":
        all_cities = []
        for i in storage.all('City').values():
            all_cities.append(i.to_dict())
        return (jsonify(all_cities), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        x = City()
        for (k, v) in new.items():
            setattr(x, k, v)
        setattr(x, 'state_id', state_id)
        x.save()
        return (x.to_dict(), 201)




@app_views.route('/cities/<ident>', methods=['GET', 'PUT', 'DELETE'])
def cities_id(ident):
    """Retrieves a specific object"""
    cities = storage.all("City").values()
    for c in cities:
        if c.id == ident:
            if request.method == 'GET':
                return get_city(c)
            elif request.method == 'PUT':
                return putcity(c)
            elif request.method == 'DELETE':
                return deletecity(c)
    abort(404, 'Not found')
