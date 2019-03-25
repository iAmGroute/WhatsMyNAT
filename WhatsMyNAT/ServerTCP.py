
import logging
import socket

from .Common.Connector import Connector

log  = logging.getLogger(__name__)
logC = logging.getLogger(__name__ + ':C')

class ServerTCP:

    def __init__(self, port, address='0.0.0.0', counterpart=None, endpointC=None):
        self.counterpart = counterpart
        self.con         = Connector(log, socket.SOCK_STREAM, None, port, address)
        self.con.listen()
        self.conC        = None
        if counterpart:
            log.info('    with counterpart [{0}]:{1}'.format(*counterpart))
            if endpointC:
                log.info('    using [{0}]:{1}'.format(*endpointC))
                self.conC = Connector(logC, socket.SOCK_DGRAM, 2, endpointC[1], endpointC[0])
            else:
                self.conC = Connector(logC, socket.SOCK_DGRAM, 2, 0, self.address)

    def task(self):
        conn, addr = self.con.accept()
        reply = '{0}\n{1}\n'.format(*addr)
        with conn:
            conn.settimeout(0.2)
            try:
                data = conn.recv(64)
            except socket.timeout:
                pass
            else:
                if len(data) == 16:
                    # Received token for reverse testing
                    log.info('    with token : {0}'.format(data))
                    if self.conC:
                        for _ in range(3):
                            self.conC.sendto(data + bytes(reply, 'utf-8'), self.counterpart)
                    # TODO: append counterpart's probing address and port
                    #reply +=
            conn.sendall(bytes(reply, 'utf-8'))
