
import logging
import socket

class Connector:

    def __init__(self, log=None, socketType=socket.SOCK_DGRAM, timeout=None, port=0, address='0.0.0.0'):
        self.log = log or logging.getLogger('dummy')
        s = socket.socket(socket.AF_INET, socketType)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(timeout)
        s.bind((address, port))
        self.socket = s
        self.log.info('Started on: [{0}]:{1}'.format(address, port))

    def __del__(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.log.info('Stopped')

    def recvfrom(self, bufferSize):
        data, addr = self.socket.recvfrom(bufferSize)
        log.info('Data from: [{0}]:{1}'.format(*addr))
        return data, addr

    def sendto(self, data, endpoint):
        sentSize = self.socket.sendto(data, endpoint)
        return sentSize

    def listen(self):
        self.socket.listen()

    def accept(self):
        conn, addr = self.socket.accept()
        log.info('Connection from: [{0}]:{1}'.format(*addr))
        return conn, addr

    def recv(self, bufferSize):
        data = self.socket.recv(bufferSize)
        return data

    def connect(self, endpoint):
        self.socket.connect(endpoint)
