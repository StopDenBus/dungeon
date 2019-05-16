#!/home/michael.gusek/prog/python/twisted/twisted/bin/python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from zope.interface import implementer

from twisted.spread import pb
from twisted.cred import checkers, portal
from twisted.internet import reactor

class Dungeon:

    def __init__(self):

        self.__bla = None

class User(pb.Avatar):
    def __init__(self, name):
        print("init")

        self.name = name

        self.remote = None

    def connect(self):

        print("connected")

    def attached(self, mind):

        print("attached")

        print("mind: {}".format(mind))
        
        self.remote = mind

        #self.send("Hallo {}".format(self.name))

    def detached(self, mind):
        print("detached")
        self.remote = None

    def perspective_foo(self, arg):
        print("I am", self.name, "perspective_foo(",arg,") called on", self)

    def send(self, message):

        self.remote.callRemote("print", message)

@implementer(portal.IRealm)
class MyRealm:

    def requestAvatar(self, avatarID, mind, *interfaces):
        print("requestAvatar")
        print("mind: {}".format(mind))
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        avatar = User(avatarID)
        avatar.server = self.server
        avatar.attached(mind)
        
        return pb.IPerspective, avatar, lambda a=avatar:a.detached(mind)

realm = MyRealm()
realm.server = Dungeon()
checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
checker.addUser("user1", "pass1".encode('utf-8'))
p = portal.Portal(realm, [checker])

reactor.listenTCP(8800, pb.PBServerFactory(p))
reactor.run()