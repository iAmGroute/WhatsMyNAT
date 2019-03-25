
import sys
import logging
import socket

from Servers.ServerUDP import ServerUDP

log = logging.getLogger(__name__)

def main(port, address, counterpart, endpointC):
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
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 serverUDP.py <port> [<nicAddress>] [<cAddress> <cPort>] [<cePort>] [<ceAddress>]')
    else:
        main(*config)
