#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.BasicObject import *
from lib.Money import *

class Container(BasicObject):

	def __init__(self, identity):

		BasicObject.__init__(self, identity)

		self.__items = [ ]

	def addItem(self, item):

		self.__items.append(item)

		item.setContainer(self)

	def removeItem(self, item):

		self.__items.remove(item)

	def getItems(self):

		return self.__items

	def findMoney(self):

		for item in self.__items:

			if "münze" in item.getIdentities():

				return item

		money = Money()

		self.addItem(money)

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

	def getData(self):

		data = BasicObject.getData(self)

		for item in self.__items:
			
			item_data = item.getData()
			
			item_class = item.getClassPath()
			
			if not item_class in data['items']:
				
				data['items'][item_class] = []
				
			data['items'][item_class].append(item_data)

		return data

	def setData(self, data):

		BasicObject.setData(self, data)
		
		if 'items' in data:
			
			for item_type in data['items']:
				
				item_class = item_type
				
				for item_data in data['items'][item_type]:
					
					item = import_class(item_class)
					
					item.setData(item_data)
					
					item.setContainer(self)
					
					self.__items.append(item)