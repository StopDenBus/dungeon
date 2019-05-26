#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import *
from random import randint

from lib.BasicObject import *

class Fruit(BasicObject):

	def __init__(self):

		super().__init__()

		self.addCommand('iss', lambda player, what, instance: self.commandEat(what))

		self.__healthiness = 0

	def getHealthiness(self):

		return self.__healthiness

	def setHealthiness(self, healthiness):

		self.__healthiness = healthiness

	def getDescription(self):

		if self.getHealthiness() > 0:

			return "%s\n%s heilt %s Lebenspunkte." % (BasicObject.getDescription(self), "Sie" if BasicObject.getGender(self) == FEMALE else "Er", self.getHealthiness())

		else:

			return BasicObject.getDescription(self)

	def commandEat(self, what):

		result = {}

		result['message'] = "Du isst %s %s." % ("die" if self.getGender() == FEMALE else "den", what.capitalize())

		result['destroy'] = True

		result['heal'] = self.getHealthiness()

		return result

class Banane(Fruit):
	
	def __init__(self):

		super().__init__()

		self.setName("banane")

		self.setGender(FEMALE)

		self.setDescription("Eine schöne gelbe Banane. Du kannst sie essen.")

		self.setShortDescription("Eine Banane.")

		self.setWeight(2)

		self.setHealthiness(randint(3,6))

		self.setValue(randint(8,11))

		self.setSingular('Banane')

		self.setPlural('Bananen')
		
	