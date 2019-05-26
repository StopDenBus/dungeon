#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.Weapon import *

class Knife(Weapon):

	def __init__(self):

		super().__init__()

		self.setGender(FEMALE)

		self.addIdentity('messer')
