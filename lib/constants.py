#!/usr/bin/python
# -*- coding: utf-8 -*-

import importlib
import sys

sys.path.append('../')

from lib.Exception import *

FEMALE = 0
MALE = 1
NEUTER = 2

GENDER = [ FEMALE, MALE, NEUTER ]

TEXT_WRAP = 80


HEALTH_VALUE = {
	100: [ 'ist absolut fit' ],
	90:  [ 'ist leicht geschwächt', 'ist schon etwas geschwächt', 'ist schon ein wenig schwächer' ],
	80:  [ 'fühlte sich auch schon besser', 'fühlte sich heute auch schon besser', 'fühlte sich heute schon besser' ],
	70:  [ 'ist leicht angekratzt', 'sieht ein wenig angekratzt aus', 'ist leicht angeschlagen' ],
	60:  [ 'ist nicht mehr taufrisch', 'sieht nicht mehr taufrisch aus', 'ist deutlich angekratzt' ],
	50:  [ 'sieht recht mitgenommen aus', 'macht einen mitgenommenen Eindruck' ],
	40:  [ 'schwankt und wankt', 'wankt bereits bedenklich' ],
	30:  [ 'ist in keiner guten Verfassung', 'war auch schon in besserer Verfassung', 'war auch schon mal besser drauf', 'war auch schon mal deutlich besser drauf' ],
	20:  [ 'braucht dringend ärztliche Behandlung', 'braucht dringend einen Arzt' ],
	10:  [ 'ist schon so gut wie bei Lars', 'steht auf der Schwelle des Todes' ]
}

def singleton(cls, *args, **kw):

	instances = {}

	def _singleton():

		if cls not in instances:

			instances[cls] = cls(*args, **kw)

		return instances[cls]

	return _singleton

def import_class(my_module):

    module_path = my_module.split(".")

    module_dir_path = ".".join(module_path[0:-1])

    my_class = module_path[-1]

    module = importlib.import_module(module_dir_path)

    my_class = getattr(module, my_class)

    my_instance = my_class()

    return my_instance

def getObjectByInstance(objects, argument_parser):
	"""
	returns an object from a list by its position
		:param objects: list of objects
		:param argument_parser: InputParser() instance
	"""
	
	# get objects instance
	instance = argument_parser.getObjectInstance()

	try:
			
		# get object from list
		object = objects[instance - 1]

	# wrong index
	except IndexError:

		raise ObjectIndexException()

	return object


def findObjectByIdentity(id, player, argument_parser, search_in_player=False):
	"""
	docstring here
		:param id: object id to find 
		:param player: current player object
		:param argument_parser: InputParser() instance
		:param search_in_player=False: look in players inventory too
	"""

	# look for a object in players current room
	objects = player.current_room.getItemsbyIdentity(id)

	# some objects are found
	if len(objects) > 0:
		
		return getObjectByInstance(objects, argument_parser)

	# look for a object in players inventory
	objects = player.getItemsbyIdentity(id)

	# some objects are found
	if len(objects) > 0:

		return getObjectByInstance(objects, argument_parser)

	# nothing found
	raise NoObjectFoundException()

def getAdjective(gender):

	if gender == FEMALE:

		return "die"

	if gender == MALE:

		return "der"

	if gender == NEUTER:

		return "das"

# mich, dich, ihn, sie, es
def getAccusative(gender):

	if gender == FEMALE:

		return "sie"

	if gender == MALE:

		return "ihn"

	if gender == NEUTER:

		return "es"

# ich, du, er, sie, es
def getNominative(gender):

	if gender == FEMALE:

		return "sie"

	if gender == MALE:

		return "er"

	if gender == NEUTER:

		return "es"

# die, den, das
def getAccusativeArticle(gender):

	if gender == FEMALE:

		return "die"

	if gender == MALE:

		return "den"

	if gender == NEUTER:

		return "das"

def getDativeArticle(gender):

	if gender == FEMALE:

		return "der"

	if gender == MALE:

		return "dem"

	if gender == NEUTER:

		return "dem"
