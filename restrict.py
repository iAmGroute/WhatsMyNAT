
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
    #     ' 35 | 12345 | a_very_long_url.somewhere.example.com.  OK'

    results = []
    for i in range(len(servers)):
        dAddress, dPorts = servers[i]

        replies = []
        for j in range(len(dPorts)):
            dPort = dPorts[j]

            print(' {0:2d} | {1:5d} | {2:38}  '.format(i, dPort, dAddress), end='')

            with clientClass(port, address) as client:
                reply = client.getRepliesFrom(dAddress, dPort)

            print('OK' if reply else 'ERROR')
            replies.append(reply)

        results.append(replies)

    print('-------- Results ---------------------')
    print('  Server    |   reply received from   ')
    print(' id |  port |     address     |  port ')
    print('----|-------|-----------------|-------')
    #     ' 35 | 12345 | 123.123.123.123 | 54321 '
    for i in range(len(servers)):
        dAddress, dPorts = servers[i]
        replies          = results[i]
        for j in range(len(dPorts)):
            dPort = dPorts[j]
            for reply, ep in replies[j]:
                print(' {0:2d} | {1:5d} | {2:15} | {3:5d}'.format(i, dPort, ep[0], ep[1]))

    return Permissiveness.undetermined


def main(portTCP, portUDP, address):
    print('Running TCP permissiveness test')
    senseTCP = runTest(ClientTCP, portTCP, address)
    print()
    print('Running UDP permissiveness test')
    senseUDP = runTest(ClientUDP, portUDP, address)
    print()
    print('TCP permissiveness: ' + str(senseTCP))
    print('UDP permissiveness: ' + str(senseUDP))


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
        print('Usage: python3 restrict.py [<localPortTCP>] [<localPortUDP>] [<nicAddress>]')
    else:
        main(*config)
