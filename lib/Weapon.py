#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.BasicObject import *

class Weapon(BasicObject):

	def __init__(self, identity, gender):

		super().__init__(identity)

		self.__attack = 0

		self.__drawed = False

		self.setGender(gender)

		self.addIdentity("weapon")

		self.addCommand('zücke', lambda: self.commandDraw())

	def setAttack(self, attack):

		self.__attack = attack

	def getAttack(self):

		return self.__attack

	def setDraw(self, draw):

		self.__drawed = draw

	def getDrawed(self):

		return self.__drawed

	def getShortDescription(self):

		description = super().getShortDescription()

		if self.__drawed:

			description += " (gezückt)"

		return description

	def commandDraw(self):

		self.__drawed = True