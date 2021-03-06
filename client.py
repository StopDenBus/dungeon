#!/home/micha/prog/python/multiuser_dungeon/python/bin/python

import argparse
import os
import sys

from twisted.spread import pb
from twisted.internet import stdio, reactor
from twisted.cred import credentials, error as credError
from twisted.internet import reactor, defer
from twisted.protocols import basic
from twisted.python.failure import Failure 
from twisted.internet.defer import gatherResults

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

        self.__hostname = None

        self.__port = None

    def setUserName(self, name):

        self.__username = name

    def setPassword(self, password):

        self.__password = password

    def setHostname(self, hostname):

        self.__hostname = hostname

    def setPort(self, port):

        self.__port = port

    def remote_print(self, message):

        print(message)

    def connect(self):

        factory = pb.PBClientFactory()

        reactor.connectTCP(self.__hostname, self.__port, factory)

        #anonymousLogin = factory.login(Anonymous())
        #anonymousLogin.addCallback(connected)
        #anonymousLogin.addErrback(error, "Anonymous login failed")

        #usernameLogin = factory.login(UsernamePassword("user1", "pass1"))
        #usernameLogin.addCallback(connected)
        #usernameLogin.addErrback(error, "Username/password login failed")

        #bothDeferreds = gatherResults([anonymousLogin, usernameLogin])
        #bothDeferreds.addCallback(finished)

        def1 = factory.login(credentials.UsernamePassword(self.__username, self.__password.encode('utf-8')),
                             client=self)
        
        def1.addCallback(self.connected)
        
        def1.addErrback(self.error)
        
        deferreds = gatherResults([def1])
        
        deferreds.addCallback(self.finished)

        stdio.StandardIO(Interact(self))
        
        reactor.run()

    def connected(self, perspective):
        # this perspective is a reference to our User object.  Save a reference
        # to it here, otherwise it will get garbage collected after this call,
        # and the server will think we logged out.
        self.perspective = perspective
        #d = perspective.callRemote("joinGroup", "#NeedAFourth")
        #d.addCallback(self.gotGroup)
        
    def error(self, failure: Failure):
        
        reason = failure.trap(credError.UnauthorizedLogin)
        
        if reason == credError.UnauthorizedLogin:
            
            print("Username/password login failed.")
        
        else:
            
            print("Ups, da ist was schief gelaufen.")    
            
    def finished(self, ignored):
        
        print("finished aufgerufen: {}".format(ignored))
        
        # reactor.stop()

    def sendCommand(self, command):

        try:

            self.perspective.callRemote("doCommand", command)

        except pb.DeadReferenceError:

            print("Hoppla, Verbindung zum Server abgebrochen.")

            self.shutdown()
            
    def perspective_print(self, message):

        print(message)

    def remote_closeConnection(self, message):

        print(message)

        self.shutdown()

    def shutdown(self):

        reactor.stop()

    def clientConnectionFailed(self, connector, reason):

        print("Verbindung zum Server fehlgeschlagen. Grund: {}".format(reason))

        self.shutdown()

    def clientConnectionLost(self, connector, reason):

        print("Verbindung zum Server fehlgeschlagen. Grund: {}".format(reason))

        self.shutdown()

def main(argv):

    parser = argparse.ArgumentParser(description='Dungeon client')

    parser.add_argument('--user', action='store', dest='user', default=None, help='Username')

    parser.add_argument('--password', action='store', dest='password', default=None, help='Password')

    parser.add_argument('--host', action='store', dest='host', default='localhost', help='Gameserver name or ip')

    parser.add_argument('--port', action='store', dest='port', metavar='N', type=int, default=8800, help='Port to use')
    
    options     = parser.parse_args()
    
    user        = options.user

    password    = options.password

    hostname    = options.host

    port        = options.port

    client = Client()

    client.setUserName(user)

    client.setPassword(password)

    client.setHostname(hostname)

    client.setPort(port)

    client.connect()

#
# main app
#
if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))
