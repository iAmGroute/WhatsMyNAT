
import logging
import socket

from .Common.Connector import Connector

log  = logging.getLogger(__name__)
logC = logging.getLogger(__name__ + ':C')

class ServerUDP:

    def __init__(self, port, address='0.0.0.0', counterpart=None, endpointC=None):
        self.counterpart = counterpart
        self.con         = Connector(log, socket.SOCK_DGRAM, None, port, address)
        self.conC        = None
        if counterpart:
            log.info('    with counterpart [{0}]:{1}'.format(*counterpart))
            if endpointC:
                log.info('    using [{0}]:{1}'.format(*endpointC))
            self.conC = Connector(logC, socket.SOCK_DGRAM, 2,
                                  *(endpointC if endpointC else (self.address, 0)))

    def task(self):
        data, addr = self.con.recvfrom(64)
        reply = '{0}\n{1}\n'.format(*addr)
        if len(data) == 16:
            # Received token for reverse testing
            log.info('    with token : {0}'.format(data))
            if self.conC:
                for _ in range(3):
                    self.conC.sendto(data + bytes(reply, 'utf-8'), self.counterpart)
            # TODO: append counterpart's probing address and port
            #reply +=
        for _ in range(3):
            self.con.sendto(bytes(reply, 'utf-8'), addr)
