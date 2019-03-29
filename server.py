
import sys
import logging

from WhatsMyNAT.ServerTCP import ServerTCP
from WhatsMyNAT.ServerUDP import ServerUDP

log = logging.getLogger(__name__)

def main(serverClass, port, address, probePort, counterpart, endpointC):
    serverUDP = serverClass(port, address, probePort, counterpart, endpointC)

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

    probePort = 0
    if len(args) > 4:
        probePort = int(args[4])
        assert 0 <= probePort < 65536

    counterpart = None
    if len(args) > 6:
        cAddress = args[5]
        cPort    = int(args[6])
        assert 0 < cPort < 65536
        counterpart = (cAddress, cPort)

    cePort = 0
    if len(args) > 7:
        cePort = int(args[7])
        assert 0 <= cePort < 65536

    ceAddress = '0.0.0.0'
    if len(args) > 8:
        ceAddress = args[8]

    return serverClass, port, address, probePort, counterpart, (ceAddress, cePort)

if __name__ == '__main__':
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 server.py [TCP|UDP] <port> [<nicAddress>] [<probePort>] [<cAddress> <cPort>] [<cePort>] [<ceAddress>]')
    else:
        main(*config)
