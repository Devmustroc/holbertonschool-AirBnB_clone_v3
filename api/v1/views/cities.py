#!/usr/bin/python3
"""cities views"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def getCities(state_id):
    """
    La fonction getCities renvoie une liste de toutes les villes dans un état donné.
    La fonction accepte un paramètre, state_id.

    :param state_id : trouve l'état dans la base de données
    :return: Une liste de toutes les villes d'un état
    :doc-author: Trelent
    """

    dictionaryCityInState = storage.get("State", state_id)
    if dictionaryCityInState is None:
        abort(404)
    return (jsonify([city.to_dict() for city in dictionaryCityInState.cities]), 200)

@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def getCity(city_id):
    """
    La fonction getCity renvoie une réponse JSON contenant le dictionnaire
    représentation de l'objet ville identifié par un identifiant donné. Si aucune de ces villes
    existe, il renvoie un message d'erreur.

    :param city_id : Récupère l'objet ville du stockage
    :return: Un dictionnaire de l'objet ville
    :doc-author: Trelent
    """

    dictionaryCity = storage.get("City", city_id)
    if dictionaryCity is None:
        abort(404)
    return (jsonify(dictionaryCity.to_dict()), 200)

@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """
    La fonction deleteCity supprime un objet City de la base de données.
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
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'], strict_slashes=False)
def postCity(state_id):
    """
    La fonction postCity crée un nouvel objet city dans le moteur de stockage.
    Il recevra un state_id comme argument et créera un nouvel objet city avec
    le nom spécifié dans la charge utile JSON de la requête. Si aucun nom n'est spécifié, il
    renverra un message d'erreur.

    :param state_id : spécifiez l'état auquel appartient la ville
    :return: La représentation du dictionnaire de la ville
    :doc-author: Trelent
    """
    dictionaryState = storage.get("State", state_id)
    if dictionaryState is None:
        abort(404)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    requestState = request.get_json()
    requestState['state_id'] = state_id
    dictionaryCity = City(**requestState)
    dictionaryCity.save()
    return (make_response(jsonify(dictionaryCity.to_dict()), 201))


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def putCity(city_id):
    """
    La fonction putCity mettra à jour un objet ville dans la base de données.
        La fonction renverra une erreur 404 si l'identifiant n'est pas trouvé dans la base de données.
        La fonction renverra également une erreur 400 s'il n'y a pas de json ou un json invalide.

    :param city_id : Récupère l'objet ville
    :return: Le dictionnaire de l'objet ville avec les nouvelles valeurs
    :doc-author: Trelent
    """

    dictionaryCity = storage.get("City", city_id)
    if dictionaryCity is None:
        abort(404)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at','updated_at']:
            setattr(dictionaryCity, key, value)
    dictionaryCity.save()
    return (jsonify(dictionaryCity.to_dict()), 200)
