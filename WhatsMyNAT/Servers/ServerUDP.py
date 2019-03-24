
import sys
import logging
import socket

log = logging.getLogger(__name__)

class ServerUDP:

    def __init__(self, port, address='0.0.0.0', counterpart=None, endpointC=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.settimeout(8)
        s.bind((address, port))
        self.socket = s
        self.counterpart = counterpart
        self.endpointC   = endpointC
        self.socketC     = None
        log.info('Server started on [{0}]:{1}'.format(address, port))
        if counterpart:
            log.info('    with counterpart [{0}]:{1}'.format(*counterpart))
            if endpointC:
                log.info('    using [{0}]:{1}'.format(*endpointC))
            self.startC()
        # elif endpointC:
        #     self.startC()
        #     self.socketC.listen()
        #     log.info('    listening for counterpart on [{0}]:{1}'.format(*endpointC))

    def startC(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(2)
        s.bind(self.endpointC if self.endpointC else (self.address, 0))
        self.socketC = s
        log.info('Starting counterpart socket')

    def stopC(self):
        s = self.socketC
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        self.socketC = None
        log.info('Stopping counterpart socket')

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        log.info('Server stopped')

    def task(self):
        data, addr = self.socket.recvfrom(64)
        log.info('Connection from: [{0}]:{1}'.format(*addr))
        reply = '{0}\n{1}\n'.format(*addr)
        if len(data) == 16:
            # Received token for reverse testing
            log.info('    with token x' + data.hex())
            if self.socketC:
                for _ in range(3):
                    self.socketC.sendto(data + bytes(reply, 'utf-8'), self.counterpart)
            # TODO: append counterpart's probing address and port
            #reply +=
        for _ in range(3):
            self.socket.sendto(bytes(reply, 'utf-8'), addr)


def main(port, address):
    logging.basicConfig(format='%(created).3f [UDP.%(levelname)s] %(message)s', level=logging.INFO)

    serverUDP = ServerUDP(port, address)

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

    return port, address

if __name__ == '__main__':
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 ServerUDP.py <port> [<nicAddress>] [<cAddress>] [<cPort>] [<ceAddress>] [cePort]')
    else:
        main(*config)
