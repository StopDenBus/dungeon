#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import *

class BasicObject():

	def __init__(self):

		self.__commands = { }

		self.__container = None

		self.__description = None

		self.__gender = None

		self.__id = None

		self.__identities = [ ]

		self.__plural = None

		self.__properties = { }

		self.__short_description = None

		self.__singular = None

		self.__value = 0

		self.__weight = 0

		self.addCommand('nimm', lambda player, what, instance: self.commandTake(player))

	def getDescription(self):

		return self.__description

	def setDescription(self, description):

		self.__description = description

	def addProperty(self, key, value):

		self.__properties[key] = value

	def getProperty(self, key):

		if key in self.__properties.keys():

			return self.__properties[key]

		return None

	def setName(self, name):

		self.__name = name

		self.__id = name

		self.addIdentity(name)

	def getName(self):

		return self.__name.capitalize()

	def getWeight(self):

		return self.__weight

	def setWeight(self, weight):

		self.__weight = weight

	def getShortDescription(self):

		return self.__short_description

	def setShortDescription(self, short_description):

		self.__short_description = short_description

	def getValue(self):

		return self.__value

	def setValue(self, value):

		self.__value = value

	def getIdentities(self):

		return self.__identities

	def addIdentity(self, identity):

		self.__identities.append(identity)

	def getGender(self):

		return self.__gender

	def setGender(self, gender):

		self.__gender = gender

	def addCommand(self, command, action):

		self.__commands[command] = action

	def getCommand(self, command):

		return self.__commands[command]

	def getCommands(self):

		return self.__commands.keys()

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

	def commandTake(self, player):

		result = {}

		if ( player.getItemsWeight() + self.getWeight() ) > player.getBurden():

			result['message'] = "%s %s ist zu schwer für Dich." % ( getAdjective(self.getGender()).capitalize(), self.getId().capitalize())

		else:

			result['message'] = "Du nimmst %s %s." % ( getAdjective(self.getGender()), self.getId().capitalize())

			result['move_to_player'] = self

		return result

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