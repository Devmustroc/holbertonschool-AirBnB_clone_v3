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

@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def city_get(city_id):
    """
    La fonction city_get renvoie une réponse JSON contenant le dictionnaire
    représentation de l'objet ville identifié par un identifiant donné. Si aucune de ces villes
    existe, il renvoie un message d'erreur.

    :param city_id : Récupère l'objet ville du stockage
    :return: Un dictionnaire de l'objet ville
    :doc-author: Trelent
    """

    dictionaryCity = storage.get("City", city_id)
    if dictionaryCity is None:
        abort(404)
    return (jsonify(dictionaryCity.to_dict()))

@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """
    La fonction city_delete supprime un objet City de la base de données.
    La fonction accepte un argument, city_id, qui est l'identifiant de la ville à supprimer.

    :param city_id : identifie la ville à supprimer
    :return: Un dictionnaire jsonifié avec une clé de statut et une valeur de ok
    :doc-author: Trelent
    """

    dictionaryCity = storage.get("City", city_id)
    if dictionaryCity is None:
        abort(404)
    dictionaryCity.delete()
    storage.save()
    return (jsonify({}))
