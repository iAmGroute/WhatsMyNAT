
import logging
import threading

# from ServerUDP import ServerUDP
from ServerTCP import ServerTCP

class ThreadTCP(threading.Thread):

    def __init__(self, port, address):
        self.serverTCP = ServerTCP(port, address)

    def run(self):
        while True:
            try:
                self.serverTCP.task()
            except Exception as e:
                log.exception(e)

class Servers:

    def __init__(self, port, address='0.0.0.0'):
        self.threadTCP = ThreadTCP(port, address)
        self.threadTCP.start()
