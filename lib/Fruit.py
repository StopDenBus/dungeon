#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import *
from random import randint

from lib.BasicObject import *

class Fruit(BasicObject):

	def __init__(self, identity, gender):

		BasicObject.__init__(self, identity)

		BasicObject.setGender(self, gender)

		BasicObject.addIdentity(self, identity)

		BasicObject.addCommand(self, 'iss', lambda player, what, instance: self.commandEat(what))

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

		Fruit.__init__(self, "banane", FEMALE)

		Fruit.setDescription(self, "Eine schöne gelbe Banane. Du kannst sie essen.")

		Fruit.setShortDescription(self, "Eine Banane.")

		Fruit.setWeight(self, 2)

		Fruit.setHealthiness(self, randint(3,6))

		Fruit.setValue(self, randint(8,11))

		self.setSingular('Banane')

		self.setPlural('Bananen')
		
	