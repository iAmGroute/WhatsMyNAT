
import sys

from NatType import NatType
from .Clients.ClientTCP import ClientTCP

from Servers import servers

def main(port, address):

    clientTCP = ClientTCP(port, address)
    externals = []
    for server in servers:
        externals.append(clientTCP.getAddressFrom(*server))

    print('  Server    |     our Port      | our Address')
    print(' id | port  | local -> external |   external ')
    #     ' 35 | 12345 | 22222 -> 54321    | 123.123.123.123'
    for i in range(len(servers)):
        print(' {0:2d} | {1:5d} | {2:5d} -> {3:5d} | {4}'.format(i, servers[i], port, externals[i][0], externals[i][1]))

    kind = NatType.undetermined
    # TODO: find a way to determine if there is no NAT at all,
    #       (getting the internal address used is not trivial for all cases)
    s1p1 = externals[0]
    s1p2 = externals[1]
    s2p1 = externals[2]
    if s1p1 == s1p2 == s2p1:
        kind = NatType.fullCone
    elif s1p1 == s1p2:
        kind = NatType.ipRestricted
    else:
        # There is no way to differentiate between portRestricted
        # and symmetric without action from the server.
        kind = NatType.symmetric
    print(kind)


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
        print('Usage: python3 ClientTCP.py <localPort> [<nicAddress>]')
    else:
        main(*config)
