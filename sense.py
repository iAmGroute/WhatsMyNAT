
import sys
import random

from names import *
from WhatsMyNAT.ClientTCP import ClientTCP
from WhatsMyNAT.ClientUDP import ClientUDP

from serverList import servers

def runTest(clientClass, port, address):

    print('-------------- Server List --------------------------')
    print(' id |  port |                address                 ')
    print('----|-------|----------------------------------------')
    #     ' 35 | 12345 | a_very_long_url.somewhere.example.com'

    with clientClass(port, address) as client:
        externals = []
        for i in range(len(servers)):
            print(' {0:2d} | {1:5d} | {2}'.format(i, servers[i][1], servers[i][0]))
            externals.append(client.getAddressFrom(*servers[i]))

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

    return sense


def main(portTCP, portUDP, address):
    print('Running TCP sensitivity test')
    senseTCP = runTest(ClientTCP, portTCP, address)
    print()
    print('Running UDP sensitivity test')
    senseUDP = runTest(ClientUDP, portUDP, address)
    print()
    print('TCP sensitivity: ' + senseTCP.name)
    print('UDP sensitivity: ' + senseUDP.name)


def parseArgs(args):
    portTCP = random.randrange(10000, 65000)
    if len(args) > 1:
        portTCP = int(args[1])
        assert 0 < portTCP < 65536

    portUDP = random.randrange(10000, 65000)
    if len(args) > 2:
        portUDP = int(args[2])
        assert 0 < portUDP < 65536

    address = '0.0.0.0'
    if len(args) > 3:
        address = args[3]

    return portTCP, portUDP, address

if __name__ == '__main__':
    try:
        config = parseArgs(sys.argv)
    except Exception as e:
        print('Usage: python3 mainTCP.py [<localPortTCP>] [<localPortUDP>] [<nicAddress>]')
    else:
        main(*config)
