#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.interface import implementer

from twisted.spread import pb
from twisted.cred import checkers, portal
from twisted.internet import reactor

from lib import *
from world import *

class Dungeon:

    def __init__(self):

        self.__user_list = []

    def addUser(self, user):

        self.__user_list.append(user)

    def removeUser(self, user):

        self.__user_list.remove(user)

    def getUsers(self):

        for user in self.__user_list:

            yield user

    def getUsersByName(self, name):

        for user in self.__user_list:

            if user.getName() == name:

                return user

        return None

class User(pb.Avatar, Player):
    def __init__(self, name):

        Player.__init__(self, name, MALE)

        self.__client = None

        self.__server = None

    def setServer(self, server):

        self.__server = server

    def getServer(self):

        return self.__server

    def attached(self, mind):
        """
        called if a client attached the game
            :param self: 
            :param mind: 
        """   
        self.__client = mind

        self.__server.addUser(self)

        self.tellWorld("{} betritt die Welt.".format(self.getName()))

        self.send("Willkommen zurück {}".format(self.getName()))

        self.current_room = markath01()

        self.current_room.addPlayer(self)

    def detached(self, mind):
        """
        called if client left the game
            :param self: 
            :param mind: 
        """
        self.tellWorld("{} verlässt die Welt".format(self.getName()))

        self.__server.removeUser(self)

        self.__client = None

    def send(self, message):
        """
        sends a message to this client
            :param self: 
            :param message: Message to send
        """   

        self.__client.callRemote("print", message)

    def tellWorld(self, message):
        """
        sends a message to all clients, but self
            :param self: 
            :param message: message to send
        """
        # go through all attached clients
        for client in self.__server.getUsers():

            # skip self
            if client == self:

                continue

            # send message
            client.send(message)

    def tellRoom(self, message):
        """
        sends a message to all players in current room
            :param self: 
            :param message: message to send
        """
        for player in self.current_room.getPlayers():

            if player == self:

                continue

            player.send(message)

    def tellPlayer(self, player, message):
        """
        sends a message to a player
            :param self: 
            :param player: player to send the message
            :param message: message to send
        """   
        player.send(message)

    def perspective_doCommand(self, command):
        """
        called by remote client
        will process a command
            :param self: 
            :param command: command to process
        """
        my_command = command.split()[0]
    
        if len(command.split()) > 1:
        
            args = " ".join(command.split()[1:])
        
        else:
        
            args = ""
            
        result = self.doCommand(my_command, args)
        
        if 'message_for_player' in result:
            
            self.tellPlayer(self, result['message_for_player'])
            
        if 'message_for_player_in_room' in result:
            
            self.tellRoom(result['message_for_player_in_room'])
                
        if 'message_for_all_player' in result:
            
            self.tellWorld(result['message_for_all_player'])

    def cmdSage(self, message):

        result = {}

        result['message_for_player'] = "Du sagst: {}".format(message)

        result['message_for_player_in_room'] = "{} sagt: {}".format(self.getName(), message)

        return result

    def cmdRufe(self, message):

        result = {}

        result['message_for_player'] = "Du rufst: {}".format(message)

        result['message_for_all_player'] = "{} ruft: {}".format(self.getName(), message)

        return result

    def cmdTeile(self, args):

        args = args.split(" ")

        name = args[0]

        message = " ".join(args[2:])

        user = self.__server.getUsersByName(name)

        if user is not None:

            if user == self:

                self.tellPlayer(self, "Du bist doch nicht schizophren.")

            else:

                _message = "{} teilt Dir mit: {}".format(self.getName(), message)

                self.tellPlayer(user, _message)

                _message = "Du teilst {} mit: {}".format(name, message)

                self.tellPlayer(self, _message)

        else:

            message = "{} ist nicht anwesend.".format(name)

            self.tellPlayer(self, message)

        return {}

@implementer(portal.IRealm)
class MyRealm:

    def __init__(self):

        self.__server = None

    def setServer(self, server):

        self.__server = server

    def getServer(self):

        return self.__server

    def requestAvatar(self, avatarID, mind, *interfaces):

        if pb.IPerspective not in interfaces:
        
            raise NotImplementedError
        
        avatar = User(avatarID)
        
        avatar.setServer(self.__server)
        
        avatar.attached(mind)
        
        return pb.IPerspective, avatar, lambda a=avatar:a.detached(mind)

realm = MyRealm()
realm.setServer(Dungeon())
checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
checker.addUser("user1", "pass1".encode('utf-8'))
checker.addUser("user2", "pass2".encode('utf-8'))
p = portal.Portal(realm, [checker])
print("Server started.")
reactor.listenTCP(8800, pb.PBServerFactory(p))
reactor.run()