
import logging
import socket

from .Common.Connector import Connector

log   = logging.getLogger(__name__)
logPT = logging.getLogger(__name__ + ':PT')
logPU = logging.getLogger(__name__ + ':PU')

class Counterpart:

    def __init__(self, port, address='0.0.0.0', probePort=0, probeAddress='0.0.0.0'):
        self.con   = Connector(log, socket.SOCK_DGRAM, None, port, address)
        self.conPU = Connector(logPU, socket.SOCK_DGRAM, 2, probePort, probeAddress)

    def task(self):
        data, addr = self.con.recvfrom(1024)
        try:
            token      = data[:16]
            dest       = data[16:].decode('utf-8').split('\n')
            remoteAddr = dest[0]
            remotePort = int(dest[1])
        except Exception as e:
            log.exception(e)
            return
        log.info('    destination: [{0}]:{1}'.format(remoteAddr, remotePort))
        log.info('    with token : {0}'.format(token))

        if token[0] == b'T':
            try:
                with Connector(logPT, socket.SOCK_STREAM, 2, probePort, probeAddress) as conPT:
                    conPT.connect((remoteAddr, remotePort))
                    conPT.sendall(data)
            except Exception:
                pass
        elif token[0] == b'U':
            for _ in range(3):
                self.conPU.sendto(data, (remoteAddr, remotePort))
        else:
            log.debug('    token does not specify TCP or UDP')
