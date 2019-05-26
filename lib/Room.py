import textwrap

import sys

sys.path.append('../')

from lib.constants import *

from lib.Container import *


class Room(Container):

    def __init__(self):

        super().__init__()
        
        self.__creatures =  [ ]

        self.__commands = { }

        self.__details = { }

        self.__directions = { }
        
        self.__players = [ ]

    def getDescription(self, current_player = None):

        description = textwrap.fill(BasicObject.getDescription(self), TEXT_WRAP)
        
        description += "\nDu kannst in folgende Richtungen gehen: %s" % ', '.join(self.__directions.keys())

        for player in self.__players:

            if player == current_player:

                continue

            description += "\n{}".format(player.getShortDescription())

        if len(self.__creatures) > 0:

            for creature in self.__creatures:

                if creature == current_player:

                    continue

                description += "\n%s" % creature.getShortDescription()

        if len(self.getItems()) > 0:

            for item in self.getItems():

                description += "\n%s" % item.getShortDescription()

        return description
    
    def addDetail(self, detail, description):

        self.__details[detail] = description

    def getDetail(self, detail):

        if detail in self.__details:

            return self.__details[detail]

        else:

            return None

    def getDetails(self):

        return self.__details.keys()

    def addDirection(self, direction, room):

        self.__directions[direction] = room

    def getDirection(self, direction):

        return self.__directions[direction]

    def getDirections(self):

        return self.__directions.keys()

    def addCreature(self, creature):

        self.__creatures.append(creature)

        creature.setContainer(self)

    def removeCreature(self, creature):

        self.__creatures.remove(creature)

    def getCreatures(self):

        return self.__creatures

    # überschreibe addItem
    def addItem(self, item):

        super().addItem(item)

        commands = item.getCommands()

        for command in commands:

            if command not in self.__commands:

                self.__commands[command] = []

            self.__commands[command].append(item)

    def removeItem(self, item):
        
        super().removeItem(item)

        commands = item.getCommands()

        for command in commands:

            try:

                self.__commands[item].remove(item)

            except:

                pass

    def getContainer(self):

        container = []

        objects = self.getItems()

        for object in objects:

            if object.getProperty("__is_box__"):

                container.append(object)

        for creature in self.getCreatures():
            
                container.append(creature)

        return container

    def getContainerbyIdentity(self, identity):

        found_container = []

        all_container = self.getContainer()

        for container in all_container:

            if identity in container.getIdentities():

                found_container.append(container)

        return found_container

    def getCreaturesbyIdentity(self, identity):

        found_creatures = []

        for creature in self.__creatures:

            if identity in creature.getIdentities():

                found_creatures.append(creature)

        return found_creatures

    def getItemsbyIdentity(self, identity):

        found_items = []

        found_items.extend(super().getItemsbyIdentity(identity))

        found_items.extend(self.getCreaturesbyIdentity(identity))

        return found_items

    def enterRoom(self, player):
        """
        called after a player enter a room
            :param self: 
            :param player: player object
        """   
        message = "{} kommt herein.".format(player.getName())

        player.tellRoom(message)

    def leaveRoom(self, player, direction):
        """
        called before a player leaves a room
            :param self: 
            :param player: player object
            :param direction: direction in which the player goes
        """
        message = "{} geht nach {}.".format(player.getName(), direction.capitalize() )

        player.tellRoom(message)
    
    def addPlayer(self, player):
        """
        add a player to room
            :param self: 
            :param player: player object
        """
        self.__players.append(player)

        player.setContainer(self)

    def removePlayer(self, player):
        """
        remove's a player from room
            :param self: 
            :param player: player object
        """
        self.__players.remove(player)

    def getPlayers(self):
        """
        returns all player in current room
            :param self: 
        """
        for player in self.__players:

            yield player