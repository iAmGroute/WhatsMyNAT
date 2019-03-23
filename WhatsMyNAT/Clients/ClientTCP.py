
import sys
import logging
import socket

log = logging.getLogger(__name__)

class ClientTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.port    = port
        self.address = address
        log.info('Local address and port: [{0}]:{1}'.format(address, port))

    def getAddressFrom(self, serverAddr, serverPort):
        log.info('Connecting to server  : [{0}]:{1}'.format(serverAddr, serverPort))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.address, self.port))
            s.connect((serverAddr, serverPort))
            reply = s.recv(1024)

        log.info('Got reply from server : {0}'.format(reply))

        reply = reply.decode('utf-8').split('\n')
        externalAddr = reply[0]
        externalPort = int(reply[1])
        return externalAddr, externalPort


def main(serverAddr, serverPort, port, address):
    logging.basicConfig(format='%(created).3f [%(levelname)s] %(message)s', level=logging.INFO)

    clientTCP = ClientTCP(port, address)
    externalAddr, externalPort = clientTCP.getAddressFrom(serverAddr, serverPort)

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
        print('Usage: python3 ClientTCP.py <serverAddr> <serverPort> <localPort> [<nicAddress>]')
    else:
        main(*config)
