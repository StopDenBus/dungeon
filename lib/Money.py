#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import FEMALE

from lib.BasicObject import BasicObject

class Money(BasicObject):

	def __init__(self) -> None:

		BasicObject.__init__(self)

		self.setGender(FEMALE)

		self.setName('münze')

		self.addIdentity("münzen")

		self.setSingular("Münze")

		self.setPlural("Münzen")

		self.__count: int = 0

	def addMoney(self, count: int) -> None:

		self.__count += count

		if self.__count == 1:

			short_description = BasicObject.getSingular(self)

		else:

			short_description = BasicObject.getPlural(self)

		short_description = "%s %s." % (self.__count, short_description)

		BasicObject.setShortDescription(self, short_description)

	def getMoney(self) -> int:

		return self.__count

	def getDescription(self) -> str:

		if self.getMoney() == 0:

			return ""

		if self.getMoney() == 1:

			description = BasicObject.getSingular(self)

		else:

			description = BasicObject.getPlural(self)

		return "%s %s." % (self.getMoney(), description)
