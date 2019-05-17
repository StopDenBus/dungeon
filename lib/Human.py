#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.constants import *

from lib.BasicRace import *

class Human(BasicRace):

	def __init__(self, identity, gender):

		BasicRace.__init__(self, identity, gender)

		BasicRace.setHitpoints(self, 100)

		BasicRace.setMagicpoints(self, 75)

		BasicRace.setStrenght(self, 80)

		BasicRace.setDescription(self, "Ein ganz normaler Mensch.")

		BasicRace.setShortDescription(self, "Ein Mensch.")

		BasicRace.setGender(self, MALE)