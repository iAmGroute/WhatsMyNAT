
import logging
import socket
import os

from .Client import parseReply
from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ClientUDP:

    def __init__(self, port, address='0.0.0.0'):
        self.con = Connector(log, socket.SOCK_DGRAM, 2, port, address)

    def __enter__(self):
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        self.con.__exit__()

    def getAddressFrom(self, serverAddr, serverPort):
        token = b'0' + os.urandom(15)
        try:
            self.con.sendto(token, (serverAddr, serverPort))
            data, addr = self.con.recvfrom(1024)
            reply = parseReply(data, token)
            return reply
        except socket.error:
            return None

    def getRepliesFrom(self, serverAddr, serverPort):
        replies = []
        token = b'U' + os.urandom(15)
        try:
            self.con.sendto(token, (serverAddr, serverPort))
            while len(replies) < 9:
                data, addr = self.con.recvfrom(1024)
                reply = parseReply(data, token)
                if reply:
                    replies.append((reply, addr))
        except socket.error:
            pass
        return replies
