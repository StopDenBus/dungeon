#!/home/micha/prog/python/multiuser_dungeon/python/bin/python

import argparse
import os
import sys

from twisted.spread import pb
from twisted.internet import stdio, reactor
from twisted.cred import credentials
from twisted.protocols import basic

class Interact(basic.LineReceiver):
    delimiter = b'\n'

    def __init__(self, client):

        self.__client = client

    def connectionMade(self):

        # self.sendLine("Web checker console. Type 'help' for help.".encode("utf-8"))
        pass

    def lineReceived(self, line):

        # Ignore blank lines
        if not line: 
            
            return
        
        line = line.decode("utf-8")

        if line.lower() == "quit":
        
            self.transport.loseConnection()

        else:

            self.__client.sendCommand(line)

class Client(pb.Referenceable):

    def __init__(self):

        self.__username = None

        self.__password = None

    def setUserName(self, name):

        self.__username = name

    def setPassword(self, password):

        self.__password = password

    def remote_print(self, message):

        print(message)

    def connect(self):

        factory = pb.PBClientFactory()

        reactor.connectTCP("localhost", 8800, factory)

        def1 = factory.login(credentials.UsernamePassword(self.__username, self.__password.encode('utf-8')),
                             client=self)
        
        def1.addCallback(self.connected)

        stdio.StandardIO(Interact(self))
        
        reactor.run()

    def connected(self, perspective):
        print("connected")
        # this perspective is a reference to our User object.  Save a reference
        # to it here, otherwise it will get garbage collected after this call,
        # and the server will think we logged out.
        self.perspective = perspective
        #d = perspective.callRemote("joinGroup", "#NeedAFourth")
        #d.addCallback(self.gotGroup)

    def sendCommand(self, command):

        self.perspective.callRemote("tellWorld", command)

    def perspective_print(self, message):

        print(message)

    def gotGroup(self, group):
        print("joined group, now sending a message to all members")
        # 'group' is a reference to the Group object (through a ViewPoint)
        d = group.callRemote("send", "You can call me Al.")
        d.addCallback(self.shutdown)

    def shutdown(self):
        reactor.stop()

def main(argv):

    parser = argparse.ArgumentParser(description='Dungeon client')

    parser.add_argument('--user', action='store', dest='user', default=None, help='Username')

    parser.add_argument('--password', action='store', dest='password', default=None, help='Password')
    
    options     = parser.parse_args()
    
    user        = options.user

    password    = options.password

    client = Client()

    client.setUserName(user)

    client.setPassword(password)

    client.connect()

#
# main app
#
if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))
