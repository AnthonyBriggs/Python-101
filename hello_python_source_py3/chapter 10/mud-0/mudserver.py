from twisted.internet.protocol import ServerFactory
from twisted.conch.telnet import StatefulTelnetProtocol
from twisted.internet import reactor

import string

class ChatProtocol(StatefulTelnetProtocol):

    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        print("New connection from", self.ip)
        self.msg_all(
            "New connection from %s" % self.ip,
            sender=None)
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost connection to", self.ip)
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        line = line.replace('\r', '')
        print(("Received line: %s from %s" % 
                (line, self.ip)))
        self.msg_all(line, sender=self)

    def msg_all(self, message, sender):
        self.factory.sendToAll(
            message, sender=sender)

    def msg_me(self, message):
        message = message.rstrip() + '\r'
        self.sendLine(message)


class ChatFactory(ServerFactory):
    protocol = ChatProtocol

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


print("Chat server running!")
factory = ChatFactory()
reactor.listenTCP(4242, factory)
reactor.run()

