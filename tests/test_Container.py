import unittest
import sys

sys.path.append('../')

#from test_BasicObject import TestBasicObject
from lib.BasicObject import BasicObject
from lib.Container import Container

class TestContainerObject(unittest.TestCase):

    def setUp(self):

        #TestBasicObject.setUp(self)

        self.object1 = BasicObject()

        self.basic_object = Container()

        self.basic_object.addItem(self.object1)

    def test_getItems(self):

        my_items = self.basic_object.getItems()

        self.assertIsInstance(my_items, list)

        self.assertIn(self.object1, my_items)

        self.assertEqual(my_items, [ self.object1 ] )

    def test_removeItem(self):

        self.basic_object.removeItem(self.object1)

        my_items = self.basic_object.getItems()

        self.assertIsInstance(my_items, list)

        self.assertEqual(my_items, [ ] )