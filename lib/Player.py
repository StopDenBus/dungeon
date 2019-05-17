#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import queue
import sys

sys.path.append('../')

class Player():

    def __init__(self, name):

        self.__name = name

    def getName(self):

        return self.__name