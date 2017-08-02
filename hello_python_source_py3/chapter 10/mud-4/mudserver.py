#!/usr/bin/python

"""
Telnet server
"""

from twisted.internet.protocol import ServerFactory
from twisted.conch.telnet import StatefulTelnetProtocol

import string

from game import Game
from player import Player

import sys

from zope.interface import implements
from twisted.internet import protocol, reactor, task
from twisted.python import log

from twisted.cred import portal
from twisted.cred import checkers
from twisted.cred import credentials

from twisted.conch.telnet import AuthenticatingTelnetProtocol
from twisted.conch.telnet import StatefulTelnetProtocol
from twisted.conch.telnet import ITelnetProtocol
from twisted.conch.telnet import TelnetTransport
from twisted.conch.telnet import ECHO


class RegisteringTelnetProtocol(AuthenticatingTelnetProtocol):
    state = "Welcome"
    
    def connectionMade(self):
        self.transport.write("Welcome to the server!\n")
        self.transport.write("(L)ogin or (R)egister a new account? ")

    def telnet_Welcome(self, line):
        if line.strip().lower() == 'r':
            self.transport.write("Enter your new username: ")
            return "NewUserName"
        elif line.strip().lower() == 'l':
            self.transport.write('Username: ')
            return "User"
        self.transport.write("I don't understand that option.")
        return 'Welcome'
     
    def telnet_NewUserName(self, line):
        for checker in list(self.portal.checkers.values()):
            print("Checking for user with name '%s' in %s" % (line, checker.users))
            if line in checker.users:
                self.transport.write("That account already exists!")
                return "Welcome"

        self.username = line
        self.transport.will(ECHO)
        self.transport.write("Enter your new password: ")
        return "NewPassword"
        
    def telnet_NewPassword(self, line):
        username, password = self.username, line
        self.addNewUser(self.username, line)
        return self.telnet_Password(line)
        
        # call the normal login method
        def login(ignored):
            creds = credentials.UsernamePassword(username, password)
            d = self.portal.login(creds, None, ITelnetProtocol)
            d.addCallback(self._cbLogin)
            d.addErrback(self._ebLogin)
        self.transport.wont(ECHO).addCallback(login)
        return 'Discard'
        
    def addNewUser(self, username, password):
        for checker in list(self.portal.checkers.values()):
            checker.addUser(username, password)
        
    def _ebLogin(self, failure):
        self.transport.write("\nAuthentication failed: %s (%s)\n" % (failure, dir(failure)))
        self.state = "Welcome"
        self.connectionMade()

class Realm:
  implements(portal.IRealm)

  def requestAvatar(self, avatarId, mind, *interfaces):
    print("Requesting avatar...")
    #print avatarId
    #print mind
    if ITelnetProtocol in interfaces:
      av = MudProtocol()
      av.name = avatarId
      av.state = "Command"
      return ITelnetProtocol, av, lambda:None
    raise NotImplementedError("Not supported by this realm")


class MudProtocol(StatefulTelnetProtocol):

    def connectionMade(self):
        self.ip = self.transport.getPeer().host

        print("New connection from", self.ip)

        self.msg_me("")
        self.msg_me("")
        self.msg_me("Welcome to the test server!")
        self.msg_me("")
        self.msg_me("This will ultimately be a mud, but give me a few days.")
        self.msg_me("If you have no idea what's going on, the mud is chapter 10 of my book.")
        self.msg_me("Check out http://manning.com/briggs/")
        self.msg_me("")
        self.msg_me("To change your name, just type 'name <whatever>'")
        self.msg_me("To see who's on the server, type 'who'")
        self.msg_me("To exit, type 'quit' or 'exit'")
        self.msg_me("")
        self.msg_me("No guarantees that this server will stay up,")
        self.msg_me("since I need to reboot to fix problems. ")
        self.msg_me("Just reconnect if you get punted!")
        self.msg_me("Have fun playing!")

        self.player = Player(game, game.start_loc)
        self.player.connection = self
        self.player.name = self.name
        self.player.input_list.insert(0, "look")
        
        checker = list(portal_.checkers.values())[0]
        self.player.password = checker.users[self.player.name]
        if self.player.name in game.player_store:
            self.player.load(game.player_store[self.player.name])
        game.players.append(self.player)
        game.save()
    
    def connectionLost(self, reason):
        print("Lost connection to", self.ip)
        try:
            game.players.remove(self.player)
        except:
            pass
        try:
            del self.player
        except:
            pass
            
    def lineReceived(self, line):
        line = line.replace('\r', '')
        line = ''.join([ch for ch in line if ch in string.printable])
        self.player.input_list.insert(0, line)
        print("Received line: %s from %s (%s)" % (line, self.name, self.ip))
        return

    def msg_me(self, message):
        message = message.rstrip() + '\r'
        self.sendLine(message)
                

if __name__ == '__main__':

    print("Prototype MUD server running!")

    realm = Realm()
    portal_ = portal.Portal(realm)
    #print portal_.checkers

    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("AA", "aa")
    portal_.registerChecker(checker)
    #print dir(checker)
    #print checker.users

    def run_one_tick():
        game.run_one_tick()

    game = Game()
    game_runner = task.LoopingCall(run_one_tick)
    game_runner.start(1.0)
    
    def do_save():
        print("Saving game...", end=' ')
        game.save()
        print("done!")
        print("Updating portal passwords...")
        for player in list(game.player_store.values()):
            for checker in list(portal_.checkers.values()):
                checker.users[player['name']] = player['password']
    
    do_save()
    game_saver = task.LoopingCall(do_save)
    game_saver.start(60.0)
        
    factory = protocol.ServerFactory()
    factory.protocol = lambda: TelnetTransport(RegisteringTelnetProtocol, portal_)

    log.startLogging(sys.stdout)
    reactor.listenTCP(4242, factory)
    reactor.run()


