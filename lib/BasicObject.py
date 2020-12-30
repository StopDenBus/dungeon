#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import FEMALE
from typing import Any, Dict, List

class BasicObject():
	"""
	Basic object holds properties shared will all other objects
	"""
	def __init__(self) -> None:

		# Deprecated
		# List of commands that are assigned to this object
		self.__commands: dict = {}

		# Objects can be 'in' another ojects, e.g. inventory for players
		# saves the 'parent' object
		self.__container: BasicObject = None

		# long description of an object
		self.__description: str = None
		self.description: str

		# gender of an object
		self.__gender: int = FEMALE

		# Deprecated
		# the name of an object or player
		# just use __name
		self.__id: str = None

		# list of id's
		self.__identities: List[str] = []

		# the name of an object, player name, npc name
		self.__name: str = None

		# the name of an object if there is more than one of them in a stack
		# e.g. 'Banane'  -> 'Bananen'
		self.__plural: str = None

		# each object can have their own additional properties
		self.__properties: Dict[str, Any] = {}

		# short description of an object
		self.__short_description: str = None

		# the name of an object if there is only one of them in a stack
		# e.g. 'Bananen'  -> 'Banane'
		self.__singular: str = None

		# the value of an object
		self.__value: int = 0

		# the weight of an object
		self.__weight: int = 0

	@property
	def description(self) -> str:
		"""
		Returns the description of an object
			:param self: the object itself
		"""

		return self.description

	@description.setter
	def description(self, description: str) -> None:
		"""
		Sets the description of an object.
			:param self: the object itself
			:param description: the description to set
		"""

		self.description = description

	def getDescription(self) -> str:
		"""
		Returns the description of an object
			:param self: the object itself
		"""
		return self.__description

	def setDescription(self, description: str) -> None:
		"""
		Sets the description of an object.
			:param self: the object itself
			:param description: the description to set
		"""
		self.__description = description

	def addProperty(self, key: str, value: Any) -> None:
		"""
		Adds a property to an object
			:param self: the object itself
			:param key: the key of the property
			:param value: the value of the property, can be single value, list, dictionary, ...
		"""
		self.__properties[key] = value

	def getProperty(self, key: str) -> Any:
		"""
		Returns the value a given key, return 'None' if key not exists
			:param self: the object itself
			:param key: the key of interest
		"""
		# check if key exists
		if key in self.__properties.keys():

			# return value
			return self.__properties[key]

		# key not found, return 'None'
		return None

	def getName(self) -> str:
		"""
		Returns the capitalized name of an object
			:param self: the object itself
		"""
		return self.__name.capitalize()

	def setName(self, name: str) -> None:
		"""
		Sets the name of an object
			:param self: the object itself
			:param name: the name to set
		"""
		# set the name
		self.__name = name

		# deprecated: set the id
		self.__id = name

		# add name to list of id's
		self.addIdentity(name)

	def getWeight(self) -> int:
		"""
		Returns the weight of an object
			:param self: the object itself
		"""
		return self.__weight

	def setWeight(self, weight: int) -> None:
		"""
		Sets the weight of an object
			:param self: the object itself
			:param weight: the weight to set
		"""
		self.__weight = weight

	def getShortDescription(self) -> str:

		return self.__short_description

	def setShortDescription(self, short_description: str) -> str:

		self.__short_description = short_description

	def getValue(self) -> int:

		return self.__value

	def setValue(self, value: int) -> None:

		self.__value = value

	def getIdentities(self) -> List[str]:
     
		for id in self.__identities:
      
			yield id

	def addIdentity(self, identity: str) -> None:

		self.__identities.append(identity)

	def getGender(self) -> int:

		return self.__gender

	def setGender(self, gender: int) -> None:

		self.__gender = gender

	def addCommand(self, command: str, action: Any) -> None:

		self.__commands[command] = action

	def getCommand(self, command: str) -> Any:

		return self.__commands[command]

	def getCommands(self) -> List[str]:
     
		for command in self.__commands.keys():
      
			yield command

	def setId(self, id):

		self.__id = id

	def getId(self):

		return self.__id

	def setSingular(self, singular):

		self.__singular = singular

	def getSingular(self):

		return self.__singular

	def setPlural(self, plural):

		self.__plural = plural

	def getPlural(self):

		return self.__plural

	def setContainer(self, container):

		self.__container = container

	def getContainer(self):

		return self.__container

	def getClassPath(self):
		
		return self.__module__ + "." + self.__class__.__qualname__

	def getData(self):

		data = {}

		data['description'] = self.__description

		data['properties'] = self.__properties

		data['name'] = self.__name

		data['identities'] = self.__identities

		data['weight'] = self.__weight

		data['short_description'] = self.__short_description

		data['value'] = self.__value

		data['gender'] = self.__gender

		data['id'] = self.__id

		data['singular'] = self.__singular

		data['plural'] = self.__plural

		return data

	def setData(self, data):

		self.__description = data['description']

		self.__gender = data['gender']

		self.__id = data['id']

		self.__identities = data['identities']

		self.__name = data['name']

		self.__plural = data['plural']

		self.__properties = data['properties']

		self.__short_description = data['short_description']

		self.__singular = data['singular']

		self.__value = data['value']

		self.__weight = data['weight']