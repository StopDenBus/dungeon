#!/usr/bin/python
# -*- coding: utf-8 -*-

class Base():

	def __init__(self):

		self.__description = None

		self.__items = [ ]

		self.__properties = { }

	def getDescription(self):

		return self.__description

	def setDescription(self, description):

		self.__description = description

	def addItem(self, item):

		self.__items.append(item)

	def removeItem(self, item):

		self.__items.remove(item)

	def getItems(self):

		return self.__items

	def addProperty(self, key, value):

		self.__properties[key] = value

	def getProperty(self, key):

		if key in self.__properties.keys():

			return self.__properties[key]

		return None
		