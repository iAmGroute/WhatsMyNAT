
import logging
import socket

from ..Common.Connector import Connector

log  = logging.getLogger(__name__)
logP = logging.getLogger(__name__ + ':P')

class CounterpartUDP:

    def __init__(self, port, address='0.0.0.0', probePort=0, probeAddress='0.0.0.0'):
        self.con  = Connector(log, socket.SOCK_DGRAM, None, port, address)
        self.conP = Connector(logP, socket.SOCK_DGRAM, None, probePort, probeAddress)

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
        for _ in range(3):
            self.con.sendto(data, (remoteAddr, remotePort))
