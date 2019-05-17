#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.BasicObject import *
from lib.Money import *

class Container(BasicObject):

	def __init__(self, identity):

		BasicObject.__init__(self, identity)

	def findMoney(self):

		items = BasicObject.getItems(self)

		money_found = False

		for item in items:

			if "münze" in item.getIdentities():

				return item

		money = Money()

		BasicObject.addItem(self, money)

		return money

	def addMoney(self, count):

		money = self.findMoney()

		money.addMoney(count)

	def getMoney(self):

		money = self.findMoney()

		return money.getMoney()

	def getItemsbyIdentity(self, identity):

		found_items = []

		for item in self.getItems():

			if identity in item.getIdentities():

				found_items.append(item)

		return found_items

	def getItemsbyShortDescription(self, description):

		found_items = []

		for item in self.getItems():

			if description == item.getShortDescription():

				found_items.append(item)

		return found_items