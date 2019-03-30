
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
                reply = client.getAddressFrom(dAddress, dPort)

            print('OK' if reply else 'ERROR')
            replies.append(reply)

        results.append(replies)

    print('---------------- Results ----------------------------')
    print('  Server    |       our Port       |   our Address   ')
    print(' id |  port |    local -> external |     external    ')
    print('----|-------|----------->----------|-----------------')
    #     ' 35 | 12345 |    22222 -> 54321    | 123.123.123.123 '
    for i in range(len(servers)):
        for j in range(len(servers[i][1])):
            reply = results[i][j] if results[i][j] else ('N/A', 0)
            print(' {0:2d} | {1:5d} |    {2:5d} -> {3:5d}    | {4:15} '.format(i, servers[i][1][j], port, reply[1], reply[0]))

    print('----------- Summaries ------------')
    print(' Server |    our External         ')
    print(' id | # |  port | address         ')
    print('----|---|-------|-----------------')
    #     ' 35 | 4 | 12345 | 123.123.123.123 '
    summaries = []
    for i in range(len(results)):
        common = None
        count  = 0
        for reply in results[i]:
            if reply:
                count += 1
                if not common:
                    common = reply
                    continue
                if reply[0] != common[0]:
                    common[0] = 'N/A'
                if reply[1] != common[1]:
                    common[1] = 0
        summaries.append((count, common))
        if common:
            print(' {0:2d} | {1:1d} | {2:5d} | {3:15} '.format(i, count, common[1], common[0]))

    sense = Sensitivity.insensitive
    globalCommon = None
    portConclusive = False
    addrConclusive = False
    for count, common in summaries:
        if count:
            if count > 1:
                portConclusive = True

            if common[0] == 'N/A' or common[1] == 0:
                sense = Sensitivity.portSensitive
                break

            if not globalCommon:
                globalCommon = common
            else:
                addrConclusive = True
                if common != globalCommon:
                    sense = Sensitivity.ipSensitive

    if not (portConclusive and addrConclusive):
        sense = Sensitivity.undetermined

    return sense


def main(portTCP, portUDP, address):
    print('Running TCP sensitivity test')
    senseTCP = runTest(ClientTCP, portTCP, address)
    print()
    print('Running UDP sensitivity test')
    senseUDP = runTest(ClientUDP, portUDP, address)
    print()
    print('TCP sensitivity: ' + str(senseTCP))
    print('UDP sensitivity: ' + str(senseUDP))


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
        print('Usage: python3 sense.py [<localPortTCP>] [<localPortUDP>] [<nicAddress>]')
    else:
        main(*config)
