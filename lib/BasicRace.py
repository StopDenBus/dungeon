#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import math
import random
import textwrap
import gc
import sys

from lib.constants import *
from apscheduler.schedulers.background import BackgroundScheduler

from lib.Commands import Commands
from lib.Container import Container
from lib.Corpse import Corpse
from lib.InputParser import InputParser

class BasicRace(Container, Commands):

	def __init__(self):

		Container.__init__(self)

		Commands.__init__(self)

		self.__hitpoints = 0

		self.__max_hitpoints = 0

		self.__magicpoints = 0

		self.__max_magicpoints = 0

		# Ausdauer
		self.__endurance = 100

		# Stärke
		self.__strength = 0

		# aktueller Raum
		self.current_room = None

		# Liste alle Feinde
		self.__enemies = []

		self.__hands = ""

		self.__heartbeat = BackgroundScheduler()

		self.__heartbeat.add_job(self.__heartbeat__, 'interval', seconds=2)

		self.__heartbeat.start()

	def die(self):

		corpse = Corpse()

		self.getContainer().addItem(corpse)

		for item in self.getItems():

			self.removeItem(item)

			corpse.addItem(item)

		self.getContainer().removeCreature(self)

		self.__heartbeat.shutdown()

		del(self)

	def __heartbeat__(self):

		if self.__hitpoints < self.__max_hitpoints:

			self.__hitpoints += 1

		if self.__hitpoints > self.__max_hitpoints:

			self.__hitpoints = self.__max_hitpoints

		if self.__magicpoints < self.__max_magicpoints:

			self.__magicpoints += 1

		if self.__magicpoints > self.__max_magicpoints:

			self.__magicpoints = self.__max_magicpoints

		if len(self.__enemies) > 0:

			self.attackEnemy()

	def getHitPoints(self):

		return self.__hitpoints

	def setHitPoints(self, hitpoints):

		self.__hitpoints = hitpoints

	def getMaxHitPoints(self):

		return self.__max_hitpoints

	def setMaxHitPoints(self, hitpoints):

		self.__max_hitpoints = hitpoints

		self.__hitpoints = hitpoints

	def doDamage(self, damage):

		self.__hitpoints = self.__hitpoints - damage

		if self.__hitpoints < 0:

			self.die()

	def getMagicpoints(self):

		return self.__magicpoints

	def setMagicpoints(self, magicpoints):

		self.__magicpoints = magicpoints

	def setMaxMagicPoints(self, magicpoints):

		self.__max_magicpoints = magicpoints

	def getMaxMagicPoints(self):

		return self.__max_magicpoints

	def getEndurance(self):

		return self.__endurance

	def setEndurance(self, endurance):

		self.__endurance = endurance

	def setStrength(self, strength):

		self.__strength = strength

	def getStrength(self):

		return self.__strength

	def setHands(self, hands):

		self.__hands = hands

	def getHands(self):

		return self.__hands

	# berechnet die Tragfähigkeit
	def getBurden(self):

		burden = 300

		endurance = self.getEndurance() - 100

		endurance = endurance / 10 * 5

		return int(burden + endurance)

	def getItemsWeight(self):

		weight = 0

		for item in self.getItems():

			weight += item.getWeight()

		return weight

	def getHealthStatus(self):

		percent = self.__hitpoints * 100 / self.__max_hitpoints

		round = int(math.ceil(percent / 10.0)) * 10

		return random.choice(HEALTH_VALUE[round])

	# überschreibe Funktion
	def getDescription(self):

		description = textwrap.fill(Container.getDescription(self), TEXT_WRAP)

		description += "\n%s %s." % ( getNominative(self.getGender()).capitalize(), self.getHealthStatus() )

		if len(Container.getItems(self)) > 0:

			description += "\n%s trägt bei sich:" % ("Sie" if Container.getGender(self) == FEMALE else "Er")

			for item in Container.getItems(self):

				description += "\n%s" % item.getShortDescription()

		return description

	def getWeapons(self):

		weapons = []

		items = self.getItems()

		for item in items:

			if "weapon" in item.getIdentities():

				weapons.append(item)

		return weapons

	def getDrawedWeapon(self):

		weapon = None

		for weapon in self.getWeapons():

			if weapon.getDrawed():

				return weapon

		return weapon

	# Benötigt hier noch keine Implementierung
	def addMessage(self, message):

		pass

	def addEnemy(self, creature):

		self.__enemies.append(creature)

	def removeEnemy(self, creature):

		if creature in self.__enemies:

			self.__enemies.remove(creature)

	def getEnemies(self):

		return self.__enemies

	def attackEnemy(self):

		available_enemies = []

		current_room = self.getContainer()

		if len(self.__enemies) > 0:

			for enemy in self.__enemies:

				if enemy in current_room.getCreatures():

					available_enemies.append(enemy)

		if len(available_enemies) > 0:

			enemy = random.choice(available_enemies)

			if self.getProperty("__is_player__"):

				print("Du greifst %s %s mit %s an." % ( getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize(), self.getHands() ) )

			attack_strength = self.__strength

			weapon = self.getDrawedWeapon()

			if weapon:

				attack_strength += weapon.getAttack()

			damage = enemy.defend(self, attack_strength)

			if self.getProperty("__is_player__"):

				if damage == 0:

					print("Du verfehlst %s %s." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize()))

				if damage == 1:

					print("Du kitzelst %s %s." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize()))

				if damage > 1 and damage < 4:

					print("Du kratzt %s %s." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

				if damage > 3 and damage < 6:

					print("Du triffst %s %s." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

				if damage > 5 and damage < 11:

					print("Du triffst %s %s hart." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

				if damage > 10 and damage < 21:

					print("Du triffst %s %s sehr hart." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

				if damage > 20 and damage < 31:

					print("Du triffst %s %s krachend." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

				if damage > 30 and damage < 51:

					print("Du zerschmetterst %s %s." % (getAccusativeArticle(enemy.getGender()), enemy.getId().capitalize() ))

			if enemy.getHitPoints() < 1:

				if self.getProperty("__is_player__"):

					print("%s %s fällt tot zu Boden." % ( getAdjective(enemy.getGender()).capitalize(), enemy.getId().capitalize() ) )

				enemy.removeEnemy(self)

				self.removeEnemy(enemy)

				enemy.die()


	def defend(self, enemy, attack_strength):

		if self.getProperty("__is_player__"):

			print("%s %s greift Dich mit %s an." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize(), enemy.getHands() ) )

		damage = random.randint(0, attack_strength)

		if self.getProperty("__is_player__"):

			if damage == 0:

				print("%s %s verfehlt dich." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize()))

			if damage == 1:

				print("%s %s kitzelt dich." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize()))

			if damage > 1 and damage < 4:

				print("%s %s kratzt Dich." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

			if damage > 3 and damage < 6:

				print("%s %s trifft Dich." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

			if damage > 5 and damage < 11:

				print("%s %s trifft Dich hart." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

			if damage > 10 and damage < 21:

				print("%s %s trifft Dich sehr hart." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

			if damage > 20 and damage < 31:

				print("%s %s trifft dich krachend." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

			if damage > 30 and damage < 51:

				print("%s %s zerschmettert Dich." % (getAccusativeArticle(enemy.getGender()).capitalize(), enemy.getId().capitalize() ))

		self.setHitPoints(self.getHitPoints() - damage)

		return damage

	def getData(self):

		data = Container.getData(self)

		data['hitpoints'] = self.__hitpoints

		data['max_hitpoints'] = self.__max_hitpoints

		data['magicpoints'] = self.__magicpoints

		data['max_magicpoints'] = self.__max_magicpoints

		data['endurance'] = self.__endurance

		data['strength'] = self.__strength

		data['current_room'] = self.current_room.getClassPath()

		return data

	def setData(self, data):
		
		Container.setData(self, data)

		self.__endurance = data['endurance']

		self.__hitpoints = data['hitpoints']

		self.__magicpoints = data['magicpoints']

		self.__max_hitpoints = data['max_hitpoints']

		self.__max_magicpoints = data['max_magicpoints']

		self.__strength = data['strength']

		self.current_room = import_class(data['current_room'])

	