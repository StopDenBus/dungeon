#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import *

from lib.Base import *

class BasicObject(Base):

	def __init__(self, identity):

		Base.__init__(self)

		self.__name = identity

		self.__identities = [ ]

		self.__identities.append(identity)

		self.__weight = 0

		self.__short_description = None

		self.__value = 0

		self.__commands = { }

		self.__gender = None

		self.__id = identity

		self.__singular = None

		self.__plural = None

		self.__container = None

		self.addCommand('nimm', lambda player, what, instance: self.commandTake(player))

	def getName(self):

		return self.__name

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