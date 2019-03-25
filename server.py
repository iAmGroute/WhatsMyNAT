
import sys
import logging

from WhatsMyNAT.ServerTCP import ServerTCP
from WhatsMyNAT.ServerUDP import ServerUDP

log = logging.getLogger(__name__)

def main(serverClass, port, address, counterpart, endpointC):
    serverUDP = serverClass(port, address, counterpart, endpointC)

    while True:
        try:
            serverUDP.task()

        except KeyboardInterrupt:
            log.info('Exit requested by keyboard')
            break

        except Exception as e:
            log.exception(e)


def parseArgs(args):
    mode = args[1].upper()
    if mode == 'TCP':
        serverClass = ServerTCP
    elif mode == 'UDP':
        serverClass = ServerUDP

    port = int(args[2])
    assert 0 < port < 65536

    address = '0.0.0.0'
    if len(args) > 3:
        address = args[3]

    counterpart = None
    if len(args) > 5:
        cAddress = args[4]
        cPort    = int(args[5])
        assert 0 < cPort < 65536
        counterpart = (cAddress, cPort)

    cePort = 0
    if len(args) > 6:
        cePort = int(args[6])
        assert 0 <= cePort < 65536

    ceAddress = '0.0.0.0'
    if len(args) > 7:
        ceAddress = args[7]

    return serverClass, port, address, counterpart, (ceAddress, cePort)

if __name__ == '__main__':
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 server.py [TCP|UDP] <port> [<nicAddress>] [<cAddress> <cPort>] [<cePort>] [<ceAddress>]')
    else:
        main(*config)
