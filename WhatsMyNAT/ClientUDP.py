
import sys
import logging
import socket
# import random

from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ClientUDP:

    def __init__(self, port, address='0.0.0.0'):
        self.con = Connector(log, socket.SOCK_DGRAM, 2, port, address)

    def __enter__(self):
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        self.con.__exit__()

    @staticmethod
    def parseReply(reply):
        log.info('    content: {0}'.format(reply))
        reply = reply.decode('utf-8').split('\n')
        externalAddr = reply[0]
        externalPort = int(reply[1])
        return externalAddr, externalPort

    def getAddressFrom(self, serverAddr, serverPort):
        # token = str(random.randrange(1000000000000000, 9999999999999999))
        # self.con.sendto(bytes(token, 'utf-8'), (serverAddr, serverPort))
        self.con.sendto(b'', (serverAddr, serverPort))
        # while True:
        reply, addr = self.con.recvfrom(1024)
        return self.parseReply(reply)
