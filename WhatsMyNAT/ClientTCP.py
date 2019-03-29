
import logging
import socket
import os

from .Client import parseReply
from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ClientTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.con  = Connector(log, socket.SOCK_STREAM, 2, port, address)
        self.conL = Connector(log, socket.SOCK_STREAM, 2, port, address)
        self.conL.listen()

    def __enter__(self):
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        self.con.__exit__()
        self.conL.__exit__()

    def getAddressFrom(self, serverAddr, serverPort):
        token = b'0' + os.urandom(15)
        try:
            self.con.connect((serverAddr, serverPort))
            self.con.sendall(token)
            data = self.con.recv(1024)
            reply = parseReply(data, token)
            return reply
        except (socket.timeout, ConnectionError):
            return None

    def getRepliesFrom(self, serverAddr, serverPort):
        replies = []
        token = b'T' + os.urandom(15)
        try:
            self.con.connect((serverAddr, serverPort))
        except (socket.timeout, ConnectionError):
            log.warn('Couldn\'t connect to [{0}]:{1}'.format(address, port))
            return None

        try:
            self.con.sendall(token)
            # data = self.con.recv(1024)
            # reply = parseReply(data, token)
        except socket.timeout:
            pass

        try:
            for _ in range(3):
                conn, addr = self.conL.accept()
                with conn:
                    conn.settimeout(2)
                    data = conn.recv(64)
                    reply = parseReply(data, token)
                    if reply:
                        replies.append((reply, addr))
        except socket.timeout:
            pass

        return replies
