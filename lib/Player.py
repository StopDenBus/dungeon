#!/usr/bin/python3
# -*- coding: utf-8 -*-

import queue
import sys

sys.path.append('../')

from texttable import Texttable

from lib.BasicRace import *

class Player(BasicRace):

	def __init__(self, identity, gender):

		super().__init__(identity, gender)

		self.message_queue = queue.Queue()

		self.addIdentity("player")

		self.addProperty("__is_player__", True)

		super().setHands("bloßen Händen")

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