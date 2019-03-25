
import sys
import logging
import socket

log  = logging.getLogger(__name__)
logC = logging.getLogger(__name__ + '.C')

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


def main(port, address, counterpart, endpointC):
    logging.basicConfig(format='%(created).3f [UDP.%(levelname)s] %(message)s', level=logging.INFO)

    serverUDP = ServerUDP(port, address, counterpart, endpointC)

    while True:
        try:
            serverUDP.task()

        except KeyboardInterrupt:
            log.info('Exit requested by keyboard')
            break

        # except socket.timeout:
        #     pass

        except Exception as e:
            log.exception(e)


def parseArgs(args):
    port = int(args[1])
    assert 0 < port < 65536

    address = '0.0.0.0'
    if len(args) > 2:
        address = args[2]

    counterpart = None
    if len(args) > 4:
        cAddress = args[3]
        cPort    = int(args[4])
        assert 0 < cPort < 65536
        counterpart = (cAddress, cPort)

    cePort = 0
    if len(args) > 5:
        cePort = int(args[5])
        assert 0 <= cePort < 65536

    ceAddress = '0.0.0.0'
    if len(args) > 6:
        ceAddress = args[6]

    return port, address, counterpart, (ceAddress, cePort)

if __name__ == '__main__':
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 ServerUDP.py <port> [<nicAddress>] [<cAddress> <cPort>] [<cePort>] [<ceAddress>]')
    else:
        main(*config)
