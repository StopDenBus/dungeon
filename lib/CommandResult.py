#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from texttable import Texttable

from lib.BasicRace import *

class CommandResult():

	def __init__(self):

		pass

	def doResult(self, result):

		message = result['message']

		if 'move_object' in result and result['move_object']:

			object = result['object']

			result['source_container'].removeItem(object)

			result['destination_container'].addItem(object)

		if 'heal' in result:

			message += "\nDu erhälst %s Lebenspunkte." % ( "aber keine" if result['heal'] == 0 else result['heal'] )

		# Objekt soll zerstört werden
		if 'destroy' in result and result['destroy']:

			# wenn das Objekt in einem Container liegt
			if 'source_container' in result:

				# Objekt aus Container entfernen
				result['source_container'].removeItem(object)

			# Objekt zerstören
			del(result['object'])

		# Geld soll hinzugefügt werden
		if 'add_money' in result:

			# für jeden Geldempfänger
			for object in result['add_money'].keys():

				# Geld hinzufügen
				object.addMoney(result['add_money'][object])

		return message