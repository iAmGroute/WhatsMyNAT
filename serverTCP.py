
import sys
import logging
import socket

from WhatsMyNAT.ServerTCP import ServerTCP

log = logging.getLogger(__name__)

def main(port, address):
    serverTCP = ServerTCP(port, address)

    while True:
        try:
            serverTCP.task()

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
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 serverTCP.py <port> [<nicAddress>]')
    else:
        main(*config)
