
import logging
import socket
import os

from .Client import parseReply
from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ClientTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.con  = Connector(log, Connector.new(socket.SOCK_STREAM, 2, port, address))
        self.conL = Connector(log, Connector.new(socket.SOCK_STREAM, 2, port, address))
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
        except OSError as e:
            log.warn(e)
            return None

    def getRepliesFrom(self, serverAddr, serverPort):
        replies = []
        token = b'T' + os.urandom(15)
        try:
            self.con.connect((serverAddr, serverPort))
        except (socket.error, ConnectionError):
            log.error('Couldn\'t connect to [{0}]:{1}'.format(serverAddr, serverPort))
            return None

        try:
            self.con.sendall(token)
            data = self.con.recv(1024)
            addr = self.con.socket.getpeername()
            reply = parseReply(data, token)
            if reply:
                replies.append((reply, addr))
        except socket.error as e:
            log.warn(e)
            pass

        try:
            for _ in range(2):
                conn, addr = self.conL.accept()
                with conn:
                    conn.settimeout(2)
                    data = conn.recv(64)
                    reply = parseReply(data, token)
                    if reply:
                        replies.append((reply, addr))
        except socket.error as e:
            log.warn(e)
            pass

        return replies
