
import sys
import random
from collections import Counter

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

        result = []
        for j in range(len(dPorts)):
            print(' {0:2d} | {1:5d} | {2:38}  '.format(i, dPorts[j], dAddress), end='')

            with clientClass(port, address) as client:
                replies = client.getRepliesFrom(dAddress, dPorts[j])

            if replies:
                print('OK')
                sources = [reply[1] for reply in replies]
                result.append(list(Counter(sources).items()))
            else:
                print('ERROR')
                result.append(None)

        results.append(result)

    print('-------- Results -------------------------')
    print('  Server    |  replies received from      ')
    print(' id |  port | # |     address     |  port ')
    print('----|-------|---|-----------------|-------')
    #     ' 35 | 12345 | 3 | 123.123.123.123 | 54321 '
    for i in range(len(servers)):
        for j in range(len(servers[i][1])):
            for source, count in results[i][j] or []:
                print(' {0:2d} | {1:5d} | {2:1d} | {3:15} | {4:5d}'.format(i, servers[i][1][j], count, source[0], source[1]))

    print('----- Summaries ------')
    print('  Server    | unique  ')
    print(' id |  port | replies ')
    print('----|-------|---------')
    #     ' 35 | 12345 |    3    '
    summaries = []
    for i in range(len(servers)):
        for j in range(len(servers[i][1])):
            uc = len(results[i][j] or [])
            summaries.append(uc)
            print(' {0:2d} | {1:5d} |    {2:1d}'.format(i, servers[i][1][j], uc))

    temp = Counter(summaries)
    uc, frequency = temp.most_common(1)[0]
    frequency = 100 * frequency / (len(summaries) - temp[0])

    if uc >= 3:
        restrict = Restrictiveness.permissive
    elif uc == 2:
        restrict = Restrictiveness.ipRestricted
    elif uc == 1:
        restrict = Restrictiveness.portRestricted
    else:
        restrict = Restrictiveness.undetermined

    return restrict, frequency


def main(portTCP, portUDP, address):
    print('Running TCP restrictiveness test')
    senseTCP, fTCP = runTest(ClientTCP, portTCP, address)
    print()
    print('Running UDP restrictiveness test')
    senseUDP, fUDP = runTest(ClientUDP, portUDP, address)
    print()
    print('TCP restrictiveness: {0} | concistency: {1:3d}%'.format(senseTCP, round(fTCP)))
    print('UDP restrictiveness: {0} | concistency: {1:3d}%'.format(senseUDP, round(fUDP)))


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
