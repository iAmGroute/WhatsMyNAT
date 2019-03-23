
import logging
import socket

log = logging.getLogger(__name__)

class ServerTCP:

    def __init__(self, port, address):
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((address, port))
        self.socket.listen()

    def __del__(self):
        self.socket.shutdown(socke.SHUT_RDWR)
        self.socket.close()

    def task(self):
        conn, addr = self.socket.accept()
        with conn:
            log.info('Connection from: [{0}]:{1}'.format(*addr))
            reply = '{0}\n{1}\n'.format(*addr)
            conn.sendall(bytes(reply, 'utf-8'))
