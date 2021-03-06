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
from models.state import State
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

    def setUp(self):
        """ Sets up instace of storage and objects """
        self.new_obj = User(
                id="12345",
                first_name="shoji",
                last_name="takashima",
                email="email@ya.com",
                password="hi"
                )

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

    """ Get method """
    @unittest.skipIf(models.storage_t == 'db', "testing fs storage")
    def test_get(self):
        """ Returns an object when passing in a model """
        obj = models.storage.all()
        try:
            del_obj = obj['User.12345']
            models.storage.delete(del_obj)
            models.storage.save()
        except:
            pass
        models.storage.new(self.new_obj)
        models.storage.save()
        ret_obj = models.storage.get(User, "12345")

    @unittest.skipIf(models.storage_t == 'db', "testing fs storage")
    def test_get_string_cls(self):
        """ Returns an object when passing in a string class """
        obj = models.storage.all()
        try:
            del_obj = obj['User.12345']
            models.storage.delete(del_obj)
            models.storage.save()
        except:
            pass
        models.storage.new(self.new_obj)
        models.storage.save()
        ret_obj = models.storage.get("User", "12345")
        self.assertEqual(ret_obj, self.new_obj)

    @unittest.skipIf(models.storage_t == 'db', "testing fs storage")
    def test_get_returns_nothing(self):
        """ Returns None when passing in a invalid id """
        get_obj = models.storage.get(User, "0000")
        self.assertIsNone(get_obj)

    @unittest.skipIf(models.storage_t == 'db', "testing fs storage")
    def test_get_pass_none(self):
        """ Returns None when passing in None type """
        get_obj = models.storage.get(User, None)
        self.assertIsNone(get_obj)

    """ Count tests """

    @unittest.skipIf(models.storage_t == 'db', "Testing fs storage")
    def test_count_all(self):
        """ Counts all objects in the storage """
        original_len = len(models.storage.all())
        method_count_len = models.storage.count()
        self.assertEqual(original_len, method_count_len)

    @unittest.skipIf(models.storage_t == 'db', "Testing fs storage")
    def test_count_string_cls(self):
        """ Counts specific classes """
        original_len = len(models.storage.all("User"))
        method_count_len = models.storage.count("User")
        self.assertEqual(original_len, method_count_len)

    @unittest.skipIf(models.storage_t == 'db', "Testing fs storage")
    def test_count_substring_cls(self):
        """ Pass in an substring of a class  """
        res = models.storage.count("St")
        self.assertEqual(res, 0)

    @unittest.skipIf(models.storage_t == 'db', "Testing fs storage")
    def test_count_pass_model_cls(self):
        """ Pass in the model """
        original_len = len(models.storage.all(State))
        method_count_len = models.storage.count(State)
