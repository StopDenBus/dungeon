#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import textwrap

from lib.constants import *

from lib.Container import *

class Box(Container):

	def __init__(self, identity, gender):

		super().__init__(identity)

		self.addIdentity(identity)

		self.setGender(gender)

		self.addProperty("__is_box__", True)

		self.__opened = False

		self.addCommand('öffne', lambda: self.commandOpenBox())

		self.addCommand('schliesse', lambda: self.commandCloseBox())

	def getOpened(self):

		return self.__opened

	def getDescription(self):

		description = textwrap.fill(super().getDescription(), TEXT_WRAP)

		if self.__opened:

			items = self.getItems()

			if len(items) > 0:

				description += "\n%s enthält:" % getNominative(self.getGender()).capitalize()

				for item in items:

					description += "\n%s" % item.getShortDescription()

		else:

			description += "\n%s ist geschlossen." % getNominative(self.getGender()).capitalize()

		return description

	def commandOpenBox(self):

		result = {}

		if self.__opened:

			result['message'] = "%s %s ist bereits offen." % ( getAdjective(self.getGender()).capitalize(), self.getId().capitalize() )

		else:

			self.__opened = True

			result['message'] = "Du öffnest %s %s." % ( getAdjective(self.getGender()), self.getId().capitalize() )

		return result

	def commandCloseBox(self):

		result = {}

		if self.__opened:

			result['message'] = "Du schliesst %s %s." % ( getAdjective(self.getGender()), self.getId().capitalize() )

			self.__opened = False

		else:

			result['message'] = "%s %s ist bereits geschlossen." % ( getAdjective(self.getGender()).capitalize(), self.getId().capitalize() )

		return result