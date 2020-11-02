#!/usr/bin/python
# -*- coding: utf-8 -*-

import json 
import os
import sys
import time
import mysql.connector

from zope.interface import implementer

from twisted.spread import pb
from twisted.cred import checkers, portal, credentials, error as credError
from twisted.internet import reactor, defer
from twisted.enterprise import adbapi

from cryptography.fernet import Fernet

from lib import *
from world import *

def logMessage(severity, message):

    msg = { "message": message }

    if severity == "INFO":

        print(json.dumps(msg))

    if severity == "ERROR":

        print(json.dumps(msg), file=sys.stderr)
    

def logInfoMessage(message):

    logMessage("INFO", message)

def logErrorMessage(message):

    logMessage("ERROR", message)

class Dungeon:

    user_list = []

    def __init__(self):

        self.__user_list = []

    @classmethod
    def addUser(cls, user):

        cls.user_list.append(user)

    @classmethod
    def removeUser(cls, user):

        cls.user_list.remove(user)

    @classmethod
    def getUsers(cls):

        for user in cls.user_list:

            yield user

    @classmethod
    def getUserByName(cls, name):

        for user in cls.user_list:

            if user.getName() == name:

                return user

        return None

    @classmethod
    def shutdown(cls, timeout):

        for user in Dungeon.user_list:

            user.savePlayer()

        time.sleep(timeout)

        try:

            reactor.shutdown()

        except:

            print("exception shutdown")

class User(pb.Avatar, Player):
    def __init__(self, name, cnx):

        Player.__init__(self)

        self.setName(name)

        self.__client = None

        self.__server = None

        self.setSaveDirectory("{}/save/player/".format(os.path.abspath(os.path.dirname(__file__))))

        self.__cnx = cnx

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

        self.loadPlayer()

        Dungeon.addUser(self)

        #self.__server.addUser(self)

        self.tellWorld("{} betritt die Welt.".format(self.getName()))

        self.send("Willkommen zurück {}".format(self.getName()))

        self.current_room = markath01()

        self.current_room.addPlayer(self)

        logInfoMessage("Player {} joined.".format(self.getName()))

    def detached(self, mind):
        """
        called if client left the game
            :param self: 
            :param mind: 
        """
        print("Verbindung zu {} verloren.".format(self.getName()))

        self.tellWorld("{} verlässt die Welt".format(self.getName()))

        self.savePlayer()

        self.current_room.removePlayer(self)

        Dungeon.removeUser(self)

        #self.__server.removeUser(self)

        self.__client = None

        logInfoMessage("{} disconnected.".format(self.getName()))

    def callRemoteMethod(self, method, args):

        self.__client.callRemote(method, args)

    def send(self, message):
        """
        sends a message to this client
            :param self: 
            :param message: Message to send
        """   
        try:

            self.__client.callRemote("print", message)

        except:

            print("exception in send")

    def tellWorld(self, message):
        """
        sends a message to all clients, but self
            :param self: 
            :param message: message to send
        """
        # go through all attached clients
        for client in Dungeon.getUsers():

            # skip self
            if client == self:

                continue

            # send message
            client.send(message)

    def tellAll(self, message):

        for player in Dungeon.getUsers():

            player.send(message)

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

        if my_command == 'shutdown':

            self.cmdShutdown()
    
        if len(command.split()) > 1:
        
            args = " ".join(command.split()[1:])
        
        else:
        
            args = None
            
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

        user = Dungeon.getUserByName(name)

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

    def cmdEnde(self, args):

        self.__client.callRemote("closeConnection", "Auf Wiedersehen.")

        return {}

    def cmdShutdown(self, timeout=5):

        try:

            timeout = int(timeout)

        except:

            timeout = 5

        self.tellAll("### Game will shutdown in {} seconds ! ###".format(timeout))

        reactor.callInThread(Dungeon.shutdown(timeout))

        return {}

    def savePlayer(self):

        logInfoMessage("Saving player data.")

        data = self.getData()

        update = "UPDATE users SET data = '{}' WHERE username = '{}';".format(json.dumps(data), self.getName().lower())

        self.__cnx.runOperation(update)

        logInfoMessage(update)

    def loadPlayer(self):

        select = "SELECT data from users WHERE username = '{}'".format(self.getName().lower())

        logInfoMessage(select)

@implementer(portal.IRealm)
class MyRealm:

    def __init__(self, cnx):

        self.__server = None

        self.__cnx = cnx

    def setServer(self, server):

        self.__server = server

    def getServer(self):

        return self.__server

    def requestAvatar(self, avatarID, mind, *interfaces):

        if pb.IPerspective not in interfaces:
        
            raise NotImplementedError
        
        avatar = User(avatarID, self.__cnx)
        
        avatar.setServer(self.__server)
        
        avatar.attached(mind)
        
        return pb.IPerspective, avatar, lambda a=avatar:a.detached(mind)

@implementer(checkers.ICredentialsChecker)
class DbPasswordChecker():

    credentialInterfaces = (credentials.IUsernamePassword, credentials.IUsernameHashedPassword)
    
    def __init__(self, cnx, key):
        
        self.cnx = cnx

        self.__key = key.encode()
    
    def requestAvatarId(self, credentials):
    
        query = "select username, password from users where username = '{}'".format(credentials.username)

        return self.cnx.runQuery(query).addCallback(self._gotQueryResults, credentials)

    def _gotQueryResults(self, rows, userCredentials):
        
        if rows:
            
            userid, password = rows[0]

            f = Fernet(self.__key)

            password = f.decrypt(password.encode())
            
            return defer.maybeDeferred(
                userCredentials.checkPassword, password).addCallback(
                self._checkedPassword, userid)

        else:
            
            raise credError.UnauthorizedLogin("No such user")
    
    def _checkedPassword(self, matched, userid):
        
        if matched:
            
            return userid

        else:
            
            raise credError.UnauthorizedLogin("Bad password")

DB_ARGS = {
    'host': os.getenv('DB_HOST'),
    'db': os.getenv('DB'),
    'user': os.getenv('DB_USER'),
    'passwd': os.getenv('DB_PASSWORD'),
    }

dbpool = adbapi.ConnectionPool("mysql.connector", **DB_ARGS)

realm = MyRealm(dbpool)

realm.setServer(Dungeon())

checker = DbPasswordChecker(dbpool, os.getenv('DB_KEY'))

p = portal.Portal(realm, [checker])

logInfoMessage("Server started.")

reactor.listenTCP(8800, pb.PBServerFactory(p))

reactor.run()