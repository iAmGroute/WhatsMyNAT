
import sys
import logging
import socket

log = logging.getLogger(__name__)

class ServerTCP:

    def __init__(self, port, address='0.0.0.0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.settimeout(8)
        s.bind((address, port))
        s.listen()
        self.socket = s
        log.info('Server started on [{0}]:{1}'.format(address, port))

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        log.info('Server stopped')

    def task(self):
        conn, addr = self.socket.accept()
        with conn:
            log.info('Connection from: [{0}]:{1}'.format(*addr))
            reply = '{0}\n{1}\n'.format(*addr)
            conn.sendall(bytes(reply, 'utf-8'))


def main(port, address):
    logging.basicConfig(format='%(created).3f [TCP.%(levelname)s] %(message)s', level=logging.INFO)

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
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 ServerTCP.py <port> [<nicAddress>]')
    else:
        main(*config)
