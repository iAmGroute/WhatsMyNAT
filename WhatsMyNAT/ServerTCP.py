
import logging
import socket

from .Common.Connector import Connector

log  = logging.getLogger(__name__ + '  ')
logP = logging.getLogger(__name__ + ':P')
logC = logging.getLogger(__name__ + ':C')

class ServerTCP:

    def __init__(self, port, address='0.0.0.0', probePort=0, counterpart=None, endpointC=None):
        self.port        = port
        self.address     = address
        self.probePort   = probePort
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
                self.conC = Connector(logC, socket.SOCK_DGRAM, 2, 0, address)

    def task(self):
        conn, addr = self.con.accept()
        with conn:
            conn.settimeout(0.2)
            try:
                data = conn.recv(64)
            except socket.timeout:
                pass
            else:
                if len(data) == 16:
                    # Received token for testing
                    log.info('    with token: x{0}'.format(data.hex()))

                    data += bytes('{0}\n{1}\n'.format(*addr), 'utf-8')
                    # TODO: append counterpart's probing address and port
                    #data +=

                    # Primary reply
                    conn.sendall(data)

                    if data[0] == b'T'[0]:
                        # Same port reply
                        try:
                            with Connector(logP, socket.SOCK_STREAM, 2, self.port, self.address) as conP:
                                conP.connect(addr)
                                conP.sendall(data)
                        except Exception:
                            pass
                        # Different port reply
                        try:
                            with Connector(logP, socket.SOCK_STREAM, 2, self.probePort, self.address) as conP:
                                conP.connect(addr)
                                conP.sendall(data)
                        except Exception:
                            pass
                        # Different ip reply request from counterpart
                        if self.conC:
                            self.conC.sendto(data, self.counterpart)
