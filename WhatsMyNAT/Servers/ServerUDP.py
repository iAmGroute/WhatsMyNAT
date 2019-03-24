
import sys
import logging
import socket

log = logging.getLogger(__name__)

class ServerUDP:

    def __init__(self, port, address='0.0.0.0'):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((address, port))
        log.info('Server started on [{0}]:{1}'.format(address, port))

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        log.info('Server stopped')

    def task(self):
        data, addr = self.socket.recvfrom(1024)
        log.info('Connection from: [{0}]:{1}'.format(*addr))
        reply = '{0}\n{1}\n'.format(*addr)
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
        print('Usage: python3 ServerUDP.py <port> [<nicAddress>]')
    else:
        main(*config)
