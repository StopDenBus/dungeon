#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import textwrap

from lib.constants import *

from lib.Container import *

class Corpse(Container):

	def __init__(self):

		super().__init__("leiche")

		self.addIdentity("leiche")

		self.setGender(FEMALE)

		self.setShortDescription("Eine Leiche.")

		self.setDescription("Eine ziemlich tote Leiche und das ist auch besser so.")

		self.addProperty("__is_box__", True)

	# überschreibe Funktion
	def getDescription(self):

		description = textwrap.fill(super().getDescription(), TEXT_WRAP)

		if len(self.getItems()) > 0:

			description += "\n%s enthält:" % getNominative(self.getGender())

			for item in self.getItems():

				description += "\n%s" % item.getShortDescription()

		return description