#!/usr/bin/python
# -*- coding: utf-8 -*-

# nose2-3 -v
# python3-coverage run -m nose2 -v
# python3-coverage html --omit=env/*,tests/*,/home/michael.gusek/.local/*,/usr/lib/python3/*
# python3-coverage report --omit=env/*,tests/*,/home/michael.gusek/.local/*,/usr/lib/python3/*


import unittest
import sys

sys.path.append('../')

from lib.BasicObject import BasicObject

class TestBasicObject(unittest.TestCase):

    def setUp(self):

        self.basic_object = BasicObject()

        self.basic_object.description = 'Some description'

        #self.basic_object.setDescription('Some description')

        self.basic_object.setShortDescription("a short description")

        self.basic_object.addProperty('key', 'value')

        self.basic_object.setName('malefitz')

        self.basic_object.setWeight(50)

        self.basic_object.setValue(10)

    def test_description(self):

        description = self.basic_object.description

        self.assertIsInstance(description, str)

        self.assertEqual('Some description', description)

    def test_getDescription(self):

        description = self.basic_object.getDescription()

        self.assertIsInstance(description, str)

        self.assertEqual('Some description', description)

    def test_getProperty(self):

        my_property = self.basic_object.getProperty('key')

        self.assertIsNotNone(my_property)

        self.assertEqual(my_property, 'value')

        my_property = self.basic_object.getProperty('nonexistent')

        self.assertIsNone(my_property)

    def test_getName(self):

        my_name = self.basic_object.getName()

        self.assertIsInstance(my_name, str)

        self.assertEqual(my_name, 'Malefitz')

    def test_getWeight(self):

        my_weight = self.basic_object.getWeight()

        self.assertIsInstance(my_weight, int)

        self.assertIsNotNone(my_weight)

        self.assertEqual(my_weight, 50)

    def test_getShortDescription(self):

        my_short_description = self.basic_object.getShortDescription()

        self.assertIsInstance(my_short_description, str)

        self.assertEqual(my_short_description, 'a short description')

    def test_getValue(self):

        my_value = self.basic_object.getValue()

        self.assertIsInstance(my_value, int)

        self.assertEqual(my_value, 10)

    def test_getData(self):

        my_data = self.basic_object.getData()

        self.assertIsInstance(my_data, dict)

        self.assertIn('description', my_data)



if __name__ == '__main__':
    
    unittest.main()