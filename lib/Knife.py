#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.Weapon import *

class Knife(Weapon):

	def __init__(self, gender):

		super().__init__("messer", gender)
