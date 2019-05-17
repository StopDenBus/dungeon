# -*- coding: utf-8 -*-

from pyparsing import *

class InputParser():

	def __init__(self):

		self.__object = None

		self.__object_instance = 1

		self.__container = None

		self.__container_instance = 1

		self.__preposition = None

	def getObject(self):

		return self.__object

	def getObjectInstance(self):

		return self.__object_instance

	def getPreposition(self):

		return self.__preposition

	def getContainer(self):

		return self.__container

	def getContainerInstance(self):

		return self.__container_instance

	def toInt(self, number):

		try:

			return int(number)

		except:

			return 1

	def parseCommand(self, raw_input):

		self.__init__()

		_adjective = Word(alphas8bit+alphas)('adjective')

		_object = Word(alphas8bit+alphas)('object')

		_instance = Word(nums)('instance')

		_preposition = oneOf("aus in")('preposition')

		_container = Word(alphas8bit+alphas)('container')

		_container_instance = Word(nums)('container_instance')

		_direction = oneOf("ab")

		# gelbe banane 2 aus|in kiste 2
		parse = _adjective + _object + _instance + _preposition + _container + _container_instance

		# gelbe banane 2 aus|in kiste
		parse = parse | _adjective + _object + _instance + _preposition + _container

		# gelbe banane aus|in kiste 2
		parse = parse | _adjective + _object + _preposition + _container + _container_instance

		# gelbe banane aus|in kiste
		parse = parse | _adjective + _object + _preposition + _container

		# banane 2 aus|in kiste 2
		parse = parse | _object + _instance + _preposition + _container + _container_instance

		# banane 2 aus|in kiste
		parse = parse | _object + _instance + _preposition + _container

		# banane aus|in kiste 2
		parse = parse | _object + _preposition + _container + _container_instance

		# banane aus|in kiste
		parse = parse | _object + _preposition + _container

		parse = parse | _adjective + _object + _instance | _adjective + _object + _direction | _object + _instance + _direction | _object + _direction 

		parse = parse | _adjective + _object | _object + _instance | _object

		parser = parse.parseString(raw_input)

		if 'adjective' in parser:

			self.__object = "%s %s" % (parser['adjective'], parser['object'])

		else:

			self.__object = parser['object']

		if 'instance' in parser:

			self.__object_instance = self.toInt(parser['instance'])

		if 'container' in parser:

			self.__container = parser['container']

		if 'container_instance' in parser:

			self.__container_instance = self.toInt(parser['container_instance'])

		return

		

