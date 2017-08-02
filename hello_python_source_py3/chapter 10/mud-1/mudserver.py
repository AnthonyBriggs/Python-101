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
        self.ip = self.transport.getPeer().host
        print("New connection from", self.ip)

        self.msg_me("Welcome to the MUD server!")
        self.msg_me("")

        self.msg_all(
            "New connection from %s" % self.ip,
            sender=None)
        self.factory.clients.append(self)

        self.player = Player(game.start_loc)
        self.player.connection = self
        game.players.append(self.player)
    
    def connectionLost(self, reason):
        print("Lost connection to", self.ip)
        self.factory.clients.remove(self)
        self.msg_all( 
            "%s has left the server" % self.ip,
            sender=None)
        game.players.remove(self.player)
        del self.player
    
    def lineReceived(self, line):
        line = line.replace('\r', '')
        line = ''.join([ch for ch in line 
                    if ch in string.printable])
        self.player.input_list.insert(0, line)
        print(("Received line: %s from %s" % 
                (line, self.ip)))

    def msg_all(self, message, sender):
        self.factory.sendToAll(
            message, sender=sender)

    def msg_me(self, message):
        message = message.rstrip() + '\r'
        self.sendLine(message)


class MudFactory(ServerFactory): 
    protocol = MudProtocol 

    def __init__(self): 
        self.clients = [] 

    def sendToAll(self, message, sender): 
        message = message.rstrip() + '\r'
        for client in self.clients:
            if sender:
                client.sendLine(
                    sender.ip + ": " + message) 
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


