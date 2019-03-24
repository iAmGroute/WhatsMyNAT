
import sys

from names import *
from Clients.ClientTCP import ClientTCP
from Clients.ClientUDP import ClientUDP

from Servers import servers

def main(ClientClass, port, address):

    print()
    print('-------------- Server List --------------------------')
    print(' id |  port |                address                 ')
    print('----|-------|----------------------------------------')
    #     ' 35 | 12345 | a_very_long_url.somewhere.example.com'

    client = ClientClass(port, address)
    externals = []
    for i in range(len(servers)):
        print(' {0:2d} | {1:5d} | {2}'.format(i, servers[i][1], servers[i][0]))
        externals.append(client.getAddressFrom(*servers[i]))

    print()
    print('---------------- Results ----------------------------')
    print('  Server    |       our Port       |   our Address   ')
    print(' id |  port |    local -> external |     external    ')
    print('----|-------|----------->----------|-----------------')
    #     ' 35 | 12345 |    22222 -> 54321    | 123.123.123.123 '
    for i in range(len(servers)):
        print(' {0:2d} | {1:5d} |    {2:5d} -> {3:5d}    | {4}'.format(i, servers[i][1], port, externals[i][1], externals[i][0]))

    sense = Sensitivity.undetermined
    s1p1 = externals[0]
    s1p2 = externals[1]
    s2p1 = externals[2]
    if s1p1 == s1p2 == s2p1:
        sense = Sensitivity.insensitive
    elif s1p1 == s1p2:
        sense = Sensitivity.ipSensitive
    else:
        # There is no way to differentiate between portRestricted
        # and symmetric without action from the server.
        sense = Sensitivity.portSensitive

    print()
    print('TCP sensitivity: ' + sense.name)


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
        print('Usage: python3 mainTCP.py <localPort> [<nicAddress>]')
    else:
        main(ClientTCP, *config)
        main(ClientUDP, *config)
