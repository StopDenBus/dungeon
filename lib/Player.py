#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import queue
import sys
import textwrap

from pathlib import Path
from texttable import Texttable


sys.path.append('../')

from lib.constants import *

from lib.BasicRace import BasicRace
from lib.Container import Container
from lib.Corpse import Corpse
from lib.Exception import LoadErrorException, SaveErrorException

class Player(BasicRace):

	def __init__(self, identity, gender):

		super().__init__(identity, gender)

		self.message_queue = queue.Queue()

		self.addIdentity("player")

		self.addProperty("__is_player__", True)

		super().setHands("bloßen Händen")

		self.__title = None

		self.__save_file_directory = None

	def setSaveDirectory(self, path):

		self.__save_file_directory = path
		
	def setTitle(self, title):
		
		self.__title = title
		
	def getTitle(self):
		
		return self.__title

	def __heartbeat__(self):

		super().__heartbeat__()

		if self.getHitPoints() < (self.getMaxHitPoints()):
			
			message = "Du hast %s Lebenspunkt%s." % (self.getHitPoints(), "e" if self.getHitPoints() > 1 else "")

			self.addMessage(message)

	def die(self):

		corpse = Corpse()

		corpse.setShortDescription("Die Leiche von %s." % self.getName().capitalize())

		self.getContainer().addItem(corpse)

		for item in self.getItems():

			self.removeItem(item)

			corpse.addItem(item)

	def getDescription(self):

		description = textwrap.fill(Container.getDescription(self), TEXT_WRAP)

		return description

	def getShortDescription(self):

		return "{} {}".format(self.getName(), self.getTitle())

	def getInventory(self):

		msg = "In deinem Inventory findest Du folgende Dinge:"

		for item in self.getItems():

			msg += "\n%s" % item.getShortDescription()

		return msg

	def getInfo(self):

		table = Texttable(78)

		table.set_cols_align(["l", "r"])

		table.add_row(['Name', self.getId().capitalize()])

		table.add_row(['Lebenspunkte', "%s / %s" % ( self.getHitPoints(), self.getMaxHitPoints() )])

		table.add_row(['Tragkraft', "%s" % self.getBurden()])

		return table.draw()

	def getHands(self):

		weapon = self.getDrawedWeapon()

		if weapon != None:

			return "%s %s" % ( getDativeArticle(weapon.getGender()), weapon.getId().capitalize() )

		else:

			return super().getHands()

	def tellRoom(self, message):

		pass

	def tellWorld(self, message):

		pass

	def getData(self):

		data = BasicRace.getData(self)

		data['title'] = self.__title

		return data

	def setData(self, data):

		BasicRace.setData(self, data)

		self.__title = data['title']
		
	def exists(self):
		
		save_file = "{}/{}.json".format(self.__save_file_directory, self.getName().lower())
		
		return save_file.is_file()

	def savePlayer(self):

		save_file = "{}/{}.json".format(self.__save_file_directory, self.getName().lower())
		
		try:
			
			data = self.getData()
			
			with open(save_file, 'w') as file:
				
				json.dump(data, file, indent=4, sort_keys=True)
				
		except:
			
			raise(SaveErrorException)

		print("Data to {} saved".format(save_file))
			
	def loadPlayer(self):

		save_file = "{}/{}.json".format(self.__save_file_directory, self.getName().lower())
		
		try:
			
			with open(save_file, "r") as file:
				
				data = json.load(file)
				
		except:
			
			raise(LoadErrorException)
			
		self.setData(data)