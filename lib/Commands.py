#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from lib.BasicObject import BasicObject
from lib.Box import Box
from lib.InputParser import InputParser

from lib.constants import *

class Commands():

    def __init__(self):

        self.__input_parser = InputParser()
        
    def doCommand(self, command, args):

        if args is not None:
        
            self.__input_parser.parseCommand(args)
        
        #try:
            
        cmd = getattr(self, "cmd" + command.capitalize())
            
        return cmd(args)
            
        #except Exception as ex:

        #    print(str(ex))

        #    return { 'message_for_player': "Wie bitte ?" } 
            
    def cmdSchau(self, args):
        
        return { 'message_for_player': self.current_room.getDescription(self) }
        
    def goDirection(self, direction):
        
        result = {}
        
        if direction in self.current_room.getDirections():
            
            next_room = self.current_room.getDirection(direction)
            
            if type(next_room) is str:
                
                next_room = import_class(next_room)
                
            self.current_room.leaveRoom(self, direction)
            
            self.current_room.removePlayer(self)
            
            self.current_room = next_room
            
            self.current_room.addPlayer(self)
            
            self.current_room.enterRoom(self)
            
            message = "Du gehst nach {}.".format(direction.capitalize())
            
            message += "\n{}".format(self.current_room.getDescription(self))
                
            result['message_for_player'] = message
            
        else:
            
            result['message_for_player'] = "Dahin kannst Du nicht gehen."
            
        return result
        
    def cmdNorden(self, args):
        
        return self.goDirection('norden')
        
    def cmdNordosten(self, args):
        
        return self.goDirection('nordosten')
        
    def cmdOsten(self, args):
        
        return self.goDirection('osten')
        
    def cmdNSüdosten(self, args):
        
        return self.goDirection('südosten')
        
    def cmdSüden(self, args):
        
        return self.goDirection('süden')
        
    def cmdSüdwesten(self, args):
        
        return self.goDirection('südwesten')
        
    def cmdWesten(self, args):
        
        return self.goDirection('westen')
        
    def cmdNordwesten(self, args):
        
        return self.goDirection('nordwesten')
    
    def cmdUntersuche(self, detail):		
        
        result = {}
        
        # look at room details first
        if detail in self.current_room.getDetails():
            
            return { 'message_for_player': self.current_room.getDetail(detail) }

		# get id 
        id = self.__input_parser.getObject()
        
        try:
			
			# look for an object in current room, players inventory or in a box
            (container, my_object) = findObjectByIdentity(id, self, self.__input_parser, True)
            
            result['message_for_player'] = my_object.getDescription()
            
        except ObjectIndexException:
            
            result['message_for_player'] = "Soviele siehst Du hier nicht."
            
        except NoObjectFoundException:
            
            result['message_for_player'] = "Sowas siehst Du hier nicht."	
        
        return result

    def cmdInventar(self, args):

        return { 'message_for_player': self.getInventory() }

    def cmdNimm(self, args):

        result = {}

        # get id 
        my_object = self.__input_parser.getObject()

        try:

            (container, my_object) = findObjectByIdentity(my_object, self, self.__input_parser, False)

        except ObjectIndexException:
            
            result['message_for_player'] = "Soviele siehst Du hier nicht."
            
        except NoObjectFoundException:
            
            result['message_for_player'] = "Sowas siehst Du hier nicht."

        except ContainerNotFoundException:

            result['message_for_player'] = "{} siehst Du hier nicht.".format(self.__input_parser.getContainer().capitalize())

        if isinstance(my_object, BasicObject):

            if isinstance(container, Box):

                if not container.isOpen():

                    result['message_for_player'] = "{} {} ist geschlossen.".format(
                        getAdjective(container.getGender()).capitalize(),
                        container.getName()
                    )

                    return result

            container.removeItem(my_object)

            self.addItem(my_object)

            my_object.setContainer(self)

            result['message_for_player'] = "Du nimmst {} {}.".format(getAdjective(my_object.getGender()), my_object.getName())

            result['message_for_player_in_room'] = "{} nimmt {} {}.".format(self.getName(), getAdjective(my_object.getGender()), my_object.getName())

        return result

    def cmdÖffne(self, args):

        result = {}

        my_box = self.__input_parser.getObject()

        try:
            
            (_, my_box) = findObjectByIdentity(args, self, self.__input_parser, False)

        except NoObjectFoundException:
            
            result['message_for_player'] = "Sowas siehst Du hier nicht."

        if isinstance(my_box, Box):

            if my_box.isOpen():

                result['message_for_player'] = "{} {} ist bereits geöffnet.".format(
                    getAdjective(my_box.getGender()).capitalize(),
                    my_box.getName(),
                )
            else:

                result['message_for_player'] = "Du öffnest {} {}.".format(
                    getAdjective(my_box.getGender()),
                    my_box.getName()
                )

                result['message_for_player_in_room'] = "{} öffnet {} {}".format(
                    self.getName(),
                    getAdjective(my_box.getGender()),
                    my_box.getName(),
                )

                my_box.openBox()
        else:

            result['message_for_player'] = "{} {} kannst Du nicht öffnen.".format(
                getAdjective(my_box.getGender()).capitalize(),
                my_box.getName(),
            )

        return result

    def cmdSchliesse(self, args):

        result = {}

        my_box = self.__input_parser.getObject()

        try:
            
            (_, my_box) = findObjectByIdentity(args, self, self.__input_parser, False)

        except NoObjectFoundException:
            
            result['message_for_player'] = "Sowas siehst Du hier nicht."

        if isinstance(my_box, Box):

            if not my_box.isOpen():

                result['message_for_player'] = "{} {} ist bereits geschlossen.".format(
                    getAdjective(my_box.getGender()).capitalize(),
                    my_box.getName(),
                )
            else:

                result['message_for_player'] = "Du schliesst {} {}.".format(
                    getAdjective(my_box.getGender()),
                    my_box.getName()
                )

                result['message_for_player_in_room'] = "{} schliesst {} {}".format(
                    self.getName(),
                    getAdjective(my_box.getGender()),
                    my_box.getName(),
                )

                my_box.closeBox()
        else:

            result['message_for_player'] = "{} {} kannst Du nicht schliessen.".format(
                getAdjective(my_box.getGender()).capitalize(),
                my_box.getName(),
            )

        return result

    def cmdSave(self, args):

        self.savePlayer()

        return { 'message_for_player': 'Deine Daten wurden gespeichert.' }

    def cmdData(self, args):

        return { 'message_for_player': self.getData() }
