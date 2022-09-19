#!/usr/bin/python3

"""
Gérer les liens de commodités et du lieu
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<string:place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def getAllAmenitiesFromPlaceByID(place_id):
    """
    La fonction getAllAmenitiesFromPlaceByID permet de
     récupérer toutes les commodités d'un lieu donné.
    Il prend un identifiant en paramètre et renvoie la liste
     de toutes les commodités pour ce lieu.
    :param place_id : Récupère l'objet de lieu à partir de la base de données
    :retour: Une liste de toutes les commodités
    :doc-author: Trelent
    """

    instancePlace = storage.get(Place, place_id)
    if instancePlace is None:
        abort(404)
    allAmenities = instancePlace.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instancePlace.amenity_ids
    listAmenities = [amenity.to_dict() for amenity in allAmenities]
    return jsonify(listAmenities), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def deleteAmenityLinkedToPlaceByID(place_id, amenity_id):
    """
    La fonction deleteAmenityLinkedToPlaceByID
    supprime un équipement d'un lieu.
    Il faut deux arguments, l'id du lieu et l'id de l'équipement à supprimer.
    Si l'un ou l'autre n'est pas trouvé, il renvoie une erreur 404.

    :param place_id : récupère l'objet lieu du stockage
    :param amenity_id : Récupère l'identifiant de l'objet d'agrément
    :return: La réponse du
    :doc-author: Trelent
    """
    instancePlace = storage.get(Place, place_id)
    if instancePlace is None:
        abort(404)
    instanceAmenity = storage.get(Amenity, amenity_id)
    if instanceAmenity is None:
        abort(404)

    allAmenities = instancePlace.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instancePlace.amenity_ids

    if instanceAmenity not in allAmenities:
        abort(404)
    allAmenities.remove(instanceAmenity)
    instancePlace.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['POST'], strict_slashes=False)
def linkAmenityToPlaceByID(place_id, amenity_id):
    """
    La fonction linkAmenityToPlaceByID lie un
    équipement à un lieu par identifiant.
    Il prend deux arguments, le place_id et le amenity_id.
    Il renvoie un dictionnaire jsonifié du nouvel équipement lié et
    un code d'état 200 en cas de succès ou 404 s'il n'est pas trouvé.
    :param place_id : identifie l'objet de lieu auquel le
    :param amenity_id : spécifiez l'identifiant de l'objet d'agrément
    :return : L'agrément qui était lié au lieu,
    et renvoie un code de statut 201
    :doc-author: Trelent
    """

    instancePlace = storage.get(Place, place_id)
    if instancePlace is None:
        abort(404)
    instanceAmenity = storage.get(Amenity, amenity_id)
    if instanceAmenity is None:
        abort(404)
    allAmenities = instancePlace.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instancePlace.amenity_ids

    if instanceAmenity in allAmenities:
        return jsonify(instanceAmenity.to_dict()), 200
    allAmenities.append(instanceAmenity)
    instancePlace.save()
    return jsonify(instanceAmenity.to_dict()), 201
