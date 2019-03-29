
import logging
import socket

from .Common.Connector import Connector

log  = logging.getLogger(__name__ + '  ')
logP = logging.getLogger(__name__ + ':P')
logC = logging.getLogger(__name__ + ':C')

class ServerUDP:

    def __init__(self, port, address='0.0.0.0', probePort=0, counterpart=None, endpointC=None):
        self.counterpart = counterpart
        self.con         = Connector(log, socket.SOCK_DGRAM, None, port, address)
        self.conP        = Connector(logP, socket.SOCK_DGRAM, 2, probePort, address)
        self.conC        = None
        if counterpart:
            log.info('    with counterpart [{0}]:{1}'.format(*counterpart))
            if endpointC:
                log.info('    using [{0}]:{1}'.format(*endpointC))
                self.conC = Connector(logC, socket.SOCK_DGRAM, 2, endpointC[1], endpointC[0])
            else:
                self.conC = Connector(logC, socket.SOCK_DGRAM, 2, 0, self.address)

    def task(self):
        data, addr = self.con.recvfrom(64)
        if len(data) == 16:
            # Received token for testing
            log.info('    with token: x{0}'.format(data.hex()))

            data += bytes('{0}\n{1}\n'.format(*addr), 'utf-8')
            # TODO: append counterpart's probing address and port
            #data +=

            # Primary reply
            for _ in range(3):
                self.con.sendto(data, addr)

            if data[0] == b'U'[0]:
                # Different port reply
                for _ in range(3):
                    self.conP.sendto(data, addr)
                # Different ip reply request from counterpart
                if self.conC:
                    self.conC.sendto(data, self.counterpart)
