#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_get_valid(self):
        """
        Test that get returns the correct object when
        given a valid class and id
        """
        self.assertIs(self.storage.get(State, self.state.id), self.state)
        self.assertIs(self.storage.get(City, self.city.id), self.city)
        self.assertIs(self.storage.get(User, self.user.id), self.user)
        self.assertIs(self.storage.get(Place, self.place.id), self.place)
        self.assertIs(self.storage.get(Amenity, self.amenity.id), self.amenity)
        self.assertIs(self.storage.get(Review, self.review.id), self.review)

    def test_get_invalid(self):
        """Test that get returns None when given an invalid class or id"""
        self.assertIsNone(self.storage.get(State, "invalid"))
        self.assertIsNone(self.storage.get("Invalid", self.state.id))
        self.assertIsNone(self.storage.get("Invalid", "invalid"))

    def test_count_with_class(self):
        """
        Test that count returns the correct number of objects
        when given a valid class
        """
        self.assertEqual(self.storage.count(State), 1)
        self.assertEqual(self.storage.count(City), 1)
        self.assertEqual(self.storage.count(User), 1)
        self.assertEqual(self.storage.count(Place), 1)
        self.assertEqual(self.storage.count(Amenity), 1)
        self.assertEqual(self.storage.count(Review), 1)

    def test_count_without_class(self):
        """
        Test that count returns the correct number of objects
        when not given a class
        """
        self.assertEqual(self.storage.count(), 6)

    def test_count_invalid_class(self):
        """Test that count returns 0 when given an invalid class"""
        self.assertEqual(self.storage.count("Invalid"), 0)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
