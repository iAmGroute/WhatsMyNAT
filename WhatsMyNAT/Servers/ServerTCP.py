
import sys
import logging
import socket

log = logging.getLogger(__name__)

class ServerTCP:

    def __init__(self, port, address='0.0.0.0'):
        self.con = Connector(log, socket.SOCK_STREAM, None, port, address)
        self.con.listen()

    def task(self):
        conn, addr = self.con.accept()
        with conn:
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
