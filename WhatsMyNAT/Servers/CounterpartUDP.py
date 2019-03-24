
import sys
import logging
import socket

log = logging.getLogger(__name__)

class CounterpartUDP:

    def __init__(self, port, address='0.0.0.0', probePort=0, probeAddress='0.0.0.0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.settimeout(8)
        s.bind((address, port))
        self.socket = s
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.settimeout(8)
        s.bind((address, port))
        self.socketP = s
        log.info('Server started on [{0}]:{1}'.format(address, port))
        log.info('    probing using [{0}]:{1}'.format(probeAddress, probePort))

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        log.info('Server stopped')

    def task(self):
        data, addr = self.socket.recvfrom(1024)
        log.info('Request from: [{0}]:{1}'.format(*addr))
        try:
            token = data[:16]
            dest = data[16:].decode('utf-8').split('\n')
            remoteAddr = dest[0]
            remotePort = int(dest[1])
        except Exception as e:
            log.exception(e)
            return
        log.info('    destination: [{0}]:{1}'.format(remoteAddr, remotePort))
        log.info('    with token x' + token.hex())
        for _ in range(3):
            self.socket.sendto(data, (remoteAddr, remotePort))


def main(port, address, probePort, probeAddress):
    logging.basicConfig(format='%(created).3f [UDP.%(levelname)s] %(message)s', level=logging.INFO)

    counterpartUDP = CounterpartUDP(port, address, probePort, probeAddress)

    while True:
        try:
            counterpartUDP.task()

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

    probePort = 0
    if len(args) > 3:
        probePort = int(args[3])
        assert 0 <= probePort < 65536

    probeAddress = '0.0.0.0'
    if len(args) > 4:
        probeAddress = args[4]

    return port, address, probePort, probeAddress

if __name__ == '__main__':
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 CounterpartUDP.py <port> [<nicAddress>] [<probePort>] [<probeAddress>]')
    else:
        main(*config)
