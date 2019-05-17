#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

from lib.constants import *

from lib.BasicRace import *

class Seller(BasicRace):

	def __init__(self, identity, gender):

		super().__init__(identity, gender)

		super().setHitPoints(50)

		super().setMaxHitPoints(50)

		super().setMagicpoints(0)

		super().setDescription("Ein ganz normaler Mensch.")

		super().setShortDescription("Ein Mensch.")

		super().setGender(MALE)

		super().addIdentity("seller")

		super().addCommand('kaufe', lambda player, what, instance: self.commandBuy(player, what, instance))

		super().addCommand('verkaufe', lambda player, what, instance: self.commandSell(player, what, instance))

	# überschreibe Funktion
	def getDescription(self):

		description = textwrap.fill(Container.getDescription(self), TEXT_WRAP)

		description += "\n%s %s." % ( getNominative(self.getGender()).capitalize(), self.getHealthStatus() )

		if len(Container.getItems(self)) > 0:

			description += "\n%s trägt bei sich:" % getNominative(self.getGender()).capitalize()

			for item in self.getItems():

				if "münze" in item.getIdentities():

					description += "\n%s" % item.getShortDescription()

				else:

					description += "\n%s (%s Münzen)" % ( item.getShortDescription(), item.getValue() )

		return description

	def trade(self, buyer, seller, what, instance):

		result = {}

		player_is_buyer = False

		if 'player' in buyer.getIdentities():

			player_is_buyer = True

		found_objects = seller.getItemsbyIdentity(what)

		if len(found_objects) > 0:

			if instance > len(found_objects):

				if player_is_buyer:

					result['message'] = "Soviele hat %s %s nicht." % ( getAdjective(self.getGender()), self.getId().capitalize() )

				else:
					
					result['message'] = "Soviele hast Du nicht."					

			else:

				found_object = found_objects[instance - 1]

				# Gegenstand für den Spieler zu schwer ?
				if player_is_buyer and ((buyer.getItemsWeight() + found_object.getWeight() ) > buyer.getBurden()):				

					result['message'] = "Du kannst %s %s nicht kaufen, %s ist zu schwer für Dich." % ( getAdjective(found_object.getGender()), 
						found_object.getId().capitalize(), getAccusative(found_object.getGender()) )

					return result

				# Genug Geld dabei ?
				if buyer.getMoney() < found_object.getValue():

					if player_is_buyer:

						result['message'] = "Du hast nicht genügend Münzen."

					else:

						result['message'] = "%s %s hat nicht genügend Münzen dafür." % ( getAdjective(self.getGender()), self.getId().capitalize() )

				else:

					result['move_object'] = True

					result['source_container'] = seller

					result['destination_container'] = buyer

					result['object'] = found_object

					result['add_money'] = {}

					result['add_money'][seller] = found_object.getValue()

					result['add_money'][buyer] = found_object.getValue() * -1

					if player_is_buyer:

						result['message'] = "Du kaufst %s %s." % ( getAdjective(found_object.getGender()), found_object.getId().capitalize())
						
					else:

						result['message'] = "Du verkaufst %s %s." % ( getAdjective(found_object.getGender()), found_object.getId().capitalize())
						
		else:

			if player_is_buyer:

				result['message'] = "Sowas hat %s %s nicht vorrätig." % ( getAdjective(self.getGender()), self.getId().capitalize() )

			else:
								
				result['message'] = "Sowas hast Du nicht."

		return result

	
	def commandSell(self, player, what, instance):

		return self.trade(self, player, what, instance)

	def commandBuy(self, player, what, instance):

		return self.trade(player, self, what, instance)