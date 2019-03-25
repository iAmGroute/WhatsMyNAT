
import logging
import socket

from .Common.Connector import Connector

log = logging.getLogger(__name__)

class ServerTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.con = Connector(log, socket.SOCK_STREAM, None, port, address)
        self.con.listen()

    def task(self):
        conn, addr = self.con.accept()
        with conn:
            reply = '{0}\n{1}\n'.format(*addr)
            conn.sendall(bytes(reply, 'utf-8'))
