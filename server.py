#!/home/micha/prog/python/multiuser_dungeon/python/bin/python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from zope.interface import implementer

from twisted.spread import pb
from twisted.cred import checkers, portal
from twisted.internet import reactor

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

class User(pb.Avatar):
    def __init__(self, name):

        self.__name = name

        self.__client = None

        self.__server = None

    def setServer(self, server):

        self.__server = server

    def getServer(self):

        return self.__server

    def attached(self, mind):
        
        self.__client = mind

        self.__server.addUser(self)

        self.tellWorld("{} betritt die Welt.".format(self.__name))

        self.send("Hallo {}".format(self.__name))

    def detached(self, mind):

        self.tellWorld("{} verlässt die Welt".format(self.__name))

        self.__server.removeUser(self)

        self.__client = None

    def send(self, message):

        self.__client.callRemote("print", message)

    def tellWorld(self, message):

        self.send("tellWorld")

        for client in self.__server.getUsers():

            if client == self:

                continue

            client.send(message)

    def perspective_tellWorld(self, message):

        self.send("perspective_tellWorld")

        self.tellWorld(message)

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