
import sys
import logging

from WhatsMyNAT.ClientTCP import ClientTCP
from WhatsMyNAT.ClientUDP import ClientUDP

log = logging.getLogger(__name__)

def main(clientClass, serverAddr, serverPort, port, address):
    with clientClass(port, address) as client:
        externalAddr, externalPort = client.getAddressFrom(serverAddr, serverPort)

    log.info('External address and port: [{0}]:{1}'.format(externalAddr, externalPort))


def parseArgs(args):
    mode = args[1].upper()
    if mode == 'TCP':
        clientClass = ClientTCP
    elif mode == 'UDP':
        clientClass = ClientUDP

    serverAddr = args[2]

    serverPort = int(args[3])
    assert 0 < serverPort < 65536

    port = int(args[4])
    assert 0 < port < 65536

    address = '0.0.0.0'
    if len(args) > 5:
        address = args[5]

    return clientClass, serverAddr, serverPort, port, address

if __name__ == '__main__':
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 client.py [TCP|UDP] <serverAddr> <serverPort> <localPort> [<nicAddress>]')
    else:
        main(*config)
