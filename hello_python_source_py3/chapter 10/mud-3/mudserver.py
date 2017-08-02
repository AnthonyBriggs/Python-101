#!/usr/bin/python

"""
Telnet server
"""

from twisted.internet.protocol import ServerFactory
from twisted.conch.telnet import StatefulTelnetProtocol
from twisted.internet import reactor, task

import string

from game import Game
from player import Player


class MudProtocol(StatefulTelnetProtocol):

    def connectionMade(self):
        self.name = "Random Person"
        self.ip = self.transport.getPeer().host

        print("New connection from", self.ip)

        self.msg_me("Welcome to the test server!")
        self.msg_me("")
        self.msg_me("This will ultimately be a mud, but give me a few days.")
        self.msg_me("If you have no idea what's going on, the mud is chapter 10 of my book. \r\nCheck out http://manning.com/briggs/")
        self.msg_me("")
        self.msg_me("To change your name, just type 'name <whatever>'")
        self.msg_me("To see who's on the server, type 'who'")
        self.msg_me("To exit, type 'quit' or 'exit'")
        self.msg_me("")
        self.msg_me("No guarantees that this server will stay up, \r\n"
                    "since I need to reboot to fix problems. \r\n"
                    "Just reconnect if you get punted!")

        self.msg_all(
            "New connection from %s" % self.ip,
            sender=self)
        self.factory.clientProtocols.append(self)

        self.player = Player(game, game.start_loc)
        self.player.connection = self
        game.players.append(self.player)
    
    def connectionLost(self, reason):
        print("Lost connection to", self.ip)
        self.factory.clientProtocols.remove(self)
        self.msg_all( 
            "%s (%s) has left the server" % (self.name, self.ip),
            sender=None)
        game.players.remove(self.player)
        del self.player
    
    def lineReceived(self, line):
        line = line.replace('\r', '')
        line = ''.join([ch for ch in line if ch in string.printable])

        self.player.input_list.insert(0, line)

        print("Received line: %s from %s (%s)" % (line, self.name, self.ip))

        return

        # don't need any of this stuff...
        if line.strip() in ['quit', 'exit']:
            self.msg_all("%s has left the building!" % self.name, sender=None)
            self.msg_me("Thanks for visiting!")
            self.transport.loseConnection()
            return

        if line.startswith('name '):
            old_name = self.name
            self.name = line.split(' ', 1)[1].rstrip()
            self.msg_all(
                "%s (%s) now claims their name is %s" % 
                (old_name, self.ip, self.name),
                sender=None)
            return
        
        if line.strip() == 'who':
            self.msg_me("There are currently %s people(s) connected:" % len(self.factory.clientProtocols))
            for client in self.factory.clientProtocols:
                self.msg_me("    %s\t(%s)" % (client.name, client.ip))
            return

        self.msg_all(line, sender=self)

    def msg_all(self, message, sender):
        self.factory.sendMessageToAllClients(message, sender=sender)

    def msg_me(self, message):
        message = message.rstrip() + '\r'
        self.sendLine(message)


class MudFactory(ServerFactory): 
    protocol = MudProtocol 

    def __init__(self): 
        self.clientProtocols = [] 

    def sendMessageToAllClients(self, message, sender): 
        message = message.rstrip() + '\r'
        for client in self.clientProtocols:
            if sender:
                client.sendLine(sender.name + ": " + message) 
            else:
                client.sendLine(message) 
                
def run_one_tick():
    game.run_one_tick()

game = Game()
# game.run()

print("Prototype MUD server running!")
factory = MudFactory()
game_runner = task.LoopingCall(run_one_tick)
game_runner.start(1.0)
reactor.listenTCP(4242, factory)
reactor.run()


