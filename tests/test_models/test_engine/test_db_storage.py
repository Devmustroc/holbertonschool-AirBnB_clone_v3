#!/usr/bin/python3
'''
    Testing the file_storage module.
'''
from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import sys
from console import HBNBCommand
from os import getenv
from io import StringIO

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBstorage only")
class test_DBStorage(unittest.TestCase):
    '''
        Testing the DB_Storage class
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Initializing classes
        '''
        cls.dbstorage = inspect.getmembers(DBStorage, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        '''
            delete variables
        '''
        del cls.dbstorage
        del cls.output

    def create(self):
        '''
            Create HBNBCommand()
        '''
        return HBNBCommand()

    def test_new(self):
        '''
            Test DB new
        '''
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attr(self):
        '''
            Testing User attributes
        '''
        new = User(email="melissa@hbtn.com", password="hello")
        self.assertTrue(new.email, "melissa@hbtn.com")

    def test_dbstorage_check_method(self):
        '''
            Check methods exists
        '''
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))

    def test_dbstorage_all(self):
        '''
            Testing all function
        '''
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        new = User(email="adriel@hbtn.com", password="abc")
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_dbstorage_new_save(self):
        '''
           Testing save method
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for k, v in result.items():
            temp_list.append(k.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    def test_dbstorage_delete(self):
        '''
            Testing delete method
        '''
        new_user = User(email="haha@hehe.com", password="abc",
                        first_name="Adriel", last_name="Tolentino")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))

    def test_model_storage(self):
        '''
            Test to check if storage is an instance for DBStorage
        '''
        self.assertTrue(isinstance(storage, DBStorage))

    def test_dbstorage_get(self):
        '''
            Testing Get method
        '''
        new = State(name="Alabama")
        new.save()
        state = models.storage.get("State", str(state.id))
        self.assertEqual(state.name, "Alabama")

    def test_dbstorage_count(self):
        '''
            Testing Count method
        '''
        old_count = models.storage.count("State")
        new = State(name="Alabama")
        new.save()
        new_count = models.storage.count("State")
        self.assertEqual(old_count + 1, new_count)


class TestDocsDbStorage(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    def test_pep8_conformance_in_file_db_storage(self):
        """
        La fonction test_pep8_conformance_in_file_db_storage
        teste que le
        Le fichier models/engine/db_storage.py
        est conforme à PEP8.
        :param self : référence l'instance de classe
        :retour: Rien
        :doc-author: Trelent
        """
        pep8Style = pep8.StyleGuide(quiet=True)
        result = pep8Style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_in_file_db_storage(self):
        """
        La fonction test_pep8_conformance_in_file_db_storage
        teste que le
        le fichier db_storage.py
        est conforme aux normes PEP8. Il utilise
        le module pep8 pour vérifier
        le fichier pour les erreurs et les avertissements.
        :param self : Accéder aux variables,
        méthodes et fonctions au sein de la même classe
        :retour: 0
        :doc-author: Trelent
        """

        pep8Style = pep8.StyleGuide(quiet=True)
        result = pep8Style.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_docstring_in_db_storage_module(self):
        """
        La fonction test_docstring_in_db_storage_module
        vérifie si le module db_storage.py a une docstring.
        Il vérifie également si la docstring
        contient au moins 10 caractères.
        :param self : représente l'instance de l'objet lui-même
        :return: La docstring pour le db_storage
        :doc-author: Trelent
        """

        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_docstring_class_in_db_storage(self):
        """
        La fonction test_docstring_class_in_db_storage
        est un test qui vérifie
        que la classe DBStorage a une docstring.
        Il est important de s'assurer que
        le responsable du code comprend quel est
        le but de la classe et comment il
        fonctionne, car cela aide au développement futur et au débogage.
        :param self : représente l'instance de l'objet lui-même
        :return : un tuple contenant la valeur attendue
        et ce qui a été renvoyé par la fonction
        :doc-author: Trelent
        """

        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_docstring_function_in_dbStorage(self):
        """
        La fonction test_docstring_function_in_dbStorage
        vérifie que chaque fonction dans dbStorage a
        une docstring.
        La fonction test_docstring_class_in_dbStorage
        vérifie que chaque classe dans dbStorage a une docstring.
        :param self : référence l'instance de classe
        :return: Un test pour déterminer si la
        chaîne __doc__ est présente et non une chaîne vide
        :doc-author: Trelent
        """

        for function in self.dbStorageFunction:
            self.assertIsNot(function[1].__doc__, None,
                             "{:s} method needs a docstring"
                             .format(function[0]))
            self.assertTrue(len(function[1].__doc__) >= 1,
                            "{:s} method needs a docstring"
                            .format(function[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count(self):
        """
        La fonction test_count est un test pour
        vérifier si la fonction count fonctionne
        d'objets comptés. La fonction test_count vérifie
        également que toutes les instances sont
        compté et pas seulement un type d'instance.
        :param self : référence l'instance de classe
        :return : le nombre de toutes les instances dans la base de données
        :doc-author: Trelent
        """
        currentStateInit = models.storage.count(State)
        stateList = ["Suisse", "France", "Espagne", "Portugale"]
        for stateName in stateList:
            newState = State(name=stateName)
            newState.save()
        countStateResult = models.storage.count(State)
        self.assertEqual(countStateResult - currentStateInit,
                         len(stateList))
        allInstance = models.storage.count()
        self.assertEqual(allInstance - currentStateInit,
                         len(stateList))
        allemagneState = State(name="allemagne")
        allemagneState.save()
        countStateResult += 1
        currentCityNumber = models.storage.count(City)
        allemagneCity = ["Studgard", "Berlin"]
        for cityName in allemagneCity:
            newCity = City(name=cityName, state_id=allemagneState.id)
            newCity.save()
        countCity = models.storage.count(City)
        self.assertEqual(countCity - currentCityNumber,
                         len(allemagneCity))
        allInstance = models.storage.count()
        stateNumber = countStateResult - currentStateInit
        cityNumber = countCity - currentCityNumber
        allInstanceNumber = stateNumber + cityNumber
        self.assertEqual(allInstanceNumber, allInstance)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get(self):
        """
        La fonction test_get teste la méthode get de
        la classe de stockage.
        Il crée de nouveaux objets State, City, User,
        Place et Review et les enregistre dans
        le moteur de stockage. Il récupère ensuite
        chaque objet de la base de données en utilisant leur
        identifiants uniques (id) et les compare à leur
        objet correspondant qui a été
        enregistré en mémoire. La fonction test_get teste
        également le moment où des arguments
        non valides sont passés dans
        la méthode de stockage get.
        :param self : référence l'instance de classe
        :return: None pour montrer que l'objet
        n'est pas dans le
        :doc-author: Trelent
        """
        newState = State(name="Alemaggne")
        newCity = City(name="Berlin", state_id=newState.id)
        newUser = User(email="namme@email.com",
                       password="password")
        newPlace = Place(name="Berlin Wall",
                         city_id=newCity.id,
                         state_id=newState.id,
                         user_id=newUser.id)
        newReview = Review(text="This is a review",
                           place_id=newPlace.id,
                           user_id=newUser.id)
        newAmenity = Amenity(name="Rosenta")
        newState.save()
        newCity.save()
        newUser.save()
        newPlace.save()
        newReview.save()
        newAmenity.save()
        self.assertEqual(None, models.storage.get("azerty", "qwerty"))
        self.assertEqual(newCity, models.storage.get(City, newCity.id))
        self.assertEqual(newUser, models.storage.get(User, newUser.id))
        self.assertEqual(newPlace, models.storage.get(Place, newPlace.id))
        self.assertEqual(newReview, models.storage.get(Review, newReview.id))
        self.assertEqual(newAmenity,
                         models.storage.get(Amenity, newAmenity.id))
        self.assertEqual(None, models.storage.get(State, "Not a good ID"))
