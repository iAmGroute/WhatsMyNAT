
import logging
import socket

from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ClientTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.con = Connector(log, socket.SOCK_STREAM, 2, port, address)

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
        self.con.connect((serverAddr, serverPort))
        reply = self.con.recv(1024)
        return self.parseReply(reply)
