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

		self.addIdentity('box')

		self.setGender(gender)

		self.addProperty("__is_box__", True)

		self.__opened = False

	def isOpen(self):

		return self.__opened

	def openBox(self):

		self.__opened = True

	def closeBox(self):

		self.__opened = False

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