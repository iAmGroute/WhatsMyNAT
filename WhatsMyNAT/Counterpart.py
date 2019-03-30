
import logging
import socket

from .Common.Connector import Connector

log   = logging.getLogger(__name__ + '   ')
logPT = logging.getLogger(__name__ + ':PT')
logPU = logging.getLogger(__name__ + ':PU')

class Counterpart:

    def __init__(self, port, address='0.0.0.0', probePort=0, probeAddress='0.0.0.0'):
        self.probePort    = probePort
        self.probeAddress = probeAddress
        self.con   = Connector(log, socket.SOCK_DGRAM, None, port, address)
        self.conPU = Connector(logPU, socket.SOCK_DGRAM, 2, probePort, probeAddress)

    def task(self):
        data, addr = self.con.recvfrom(1024)
        try:
            token      = data[:16]
            dest       = data[16:].decode('utf-8').split('\n')
            remoteAddr = dest[0]
            remotePort = int(dest[1])
        except:
            return

        log.info('    with token: x{0}'.format(token.hex()))
        log.info('    destination: [{0}]:{1}'.format(remoteAddr, remotePort))

        if token[0] == b'T'[0]:
            with Connector(logPT, socket.SOCK_STREAM, 2, self.probePort, self.probeAddress) as conPT:
                try:
                    conPT.connect((remoteAddr, remotePort))
                    conPT.sendall(data)
                except (socket.error, ConnectionError) as e:
                    logPT.exception(e)
                    pass
        elif token[0] == b'U'[0]:
            for _ in range(3):
                self.conPU.sendto(data, (remoteAddr, remotePort))
        else:
            log.debug('    token does not specify TCP or UDP')
