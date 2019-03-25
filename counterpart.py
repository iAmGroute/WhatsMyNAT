
import sys
import logging

from WhatsMyNAT.Counterpart import Counterpart

log = logging.getLogger(__name__)

def main(port, address, probePort, probeAddress):
    counterpart = Counterpart(port, address, probePort, probeAddress)

    while True:
        try:
            counterpart.task()

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

    probePort = 0
    if len(args) > 3:
        probePort = int(args[3])
        assert 0 <= probePort < 65536

    probeAddress = '0.0.0.0'
    if len(args) > 4:
        probeAddress = args[4]

    return port, address, probePort, probeAddress

if __name__ == '__main__':
    logging.basicConfig(format='%(created).3f [%(name)s|%(levelname)s] %(message)s', level=logging.INFO)
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 counterpart.py <port> [<nicAddress>] [<probePort>] [<probeAddress>]')
    else:
        main(*config)
