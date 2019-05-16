#!/home/michael.gusek/prog/python/twisted/twisted/bin/python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials

def main():
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    def1 = factory.login(credentials.UsernamePassword("user1", "pass1".encode('utf-8')) )
    def1.addCallback(connected)
    print("run")
    reactor.run()

def connected(perspective):
    print("got perspective ref:", perspective)
    print("asking it to foo(12)")
    perspective.callRemote("foo", 12)

def perspective_hello(self, arg):

    print(arg)

main()