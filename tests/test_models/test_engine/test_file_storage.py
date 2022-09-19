#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count(self):
        """
        La fonction test_count est un test pour
        vérifier si la fonction count fonctionne
        correctement. Il vérifie si le nombre
        d'objets créés est égal au nombre
        d'objets comptés. La fonction test_count
        vérifie également que toutes les instances sont
        compté et pas seulement un type d'instance.
        :param self : référence l'instance de classe
        :return : le nombre de toutes
        les instances dans la base de données
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
        La fonction test_get teste la méthode get
        de la classe de stockage.
        Il crée de nouveaux objets State, City, User,
        Place et Review et les enregistre dans
        le moteur de stockage. Il récupère ensuite
        chaque objet de la base de données en utilisant leur
        identifiants uniques (id) et les compare à
        leur objet correspondant qui a été
        enregistré en mémoire. La fonction test_get
        teste également le moment où des arguments
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
