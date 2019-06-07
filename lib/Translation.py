#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from fluent.runtime import FluentBundle
from pathlib import Path

sys.path.append('../')

from lib.constants import *

class Translation():

    def __init__(self):

        self.__language = 'de'

        self.__locales = None

        self.__bundle = None

    def setLanguage(self, language):

        self.__language = language

        self.setupTranslation()

    def getLanguage(self):

        return self.__language

    def setLocaleDirectory(self, locales):

        self.__locales = locales

    def setupTranslation(self):

        messages = ""

        self.__bundle = FluentBundle([self.__language])

        path = Path("{}/{}".format(self.__locales, self.__language))

        for file in path.iterdir():
            
            with open(file, "r") as f:

                messages += f.read()

        self.__bundle.add_messages(messages)

    def addMessage(self, message):

        self.__bundle.add_messages(message)

        print("Message '{}' added.".format(message))

    def getMessage(self, id, args):

        return self.__bundle.format(id, args)
