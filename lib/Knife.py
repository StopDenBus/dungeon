#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.Weapon import Weapon
from lib.constants import FEMALE

class Knife(Weapon):

	def __init__(self) -> None:

		super().__init__()

		self.setGender(FEMALE)

		self.addIdentity('messer')
