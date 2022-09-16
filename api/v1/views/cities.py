#!/usr/bin/python3
"""cities views"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_get(state_id):
    """
    La fonction cities_get renvoie une liste de toutes les villes dans un état donné.
    La fonction accepte un paramètre, state_id.

    :param state_id : trouve l'état dans la base de données
    :return: Une liste de toutes les villes d'un état
    :doc-author: Trelent
    """

    dictionaryCityInState = storage.get("State", state_id)
    if dictionaryCityInState is None:
        abort(404)
    return jsonify([city.to_dict() for city in dictionaryCityInState.cities])
