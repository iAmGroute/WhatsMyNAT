
import sys
import logging
import socket
# import random

log = logging.getLogger(__name__)

class ClientUDP:

    def __init__(self, port, address='0.0.0.0'):
        self.port    = port
        self.address = address
        log.info('Local address and port: [{0}]:{1}'.format(address, port))

    def getAddressFrom(self, serverAddr, serverPort):
        log.info('Connecting to server  : [{0}]:{1}'.format(serverAddr, serverPort))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(2)
            s.bind((self.address, self.port))
            # token = str(random.randrange(1000000000000000, 9999999999999999))
            # s.sendto(bytes(token, 'utf-8'), (serverAddr, serverPort))
            s.sendto(b'', (serverAddr, serverPort))
            # while True:
            reply, addr = s.recvfrom(1024)

        log.info('Got reply from server : [{0}]:{1}'.format(*addr))
        log.info('    content: {0}'.format(reply))

        reply = reply.decode('utf-8').split('\n')
        externalAddr = reply[0]
        externalPort = int(reply[1])
        return externalAddr, externalPort


def main(serverAddr, serverPort, port, address):
    logging.basicConfig(format='%(created).3f [%(levelname)s] %(message)s', level=logging.INFO)

    clientUDP = ClientUDP(port, address)
    externalAddr, externalPort = clientUDP.getAddressFrom(serverAddr, serverPort)

    log.info('External address and port: [{0}]:{1}'.format(externalAddr, externalPort))


def parseArgs(args):
    serverAddr = args[1]

    serverPort = int(args[2])
    assert 0 < serverPort < 65536

    port = int(args[3])
    assert 0 < port < 65536

    address = '0.0.0.0'
    if len(args) > 4:
        address = args[4]

    return serverAddr, serverPort, port, address

if __name__ == '__main__':
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 ClientUDP.py <serverAddr> <serverPort> <localPort> [<nicAddress>]')
    else:
        main(*config)