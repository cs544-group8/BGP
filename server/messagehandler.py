#!/usr/bin/python
#Source adapted from: http://www.ual.es/~vruiz/Docencia/Apuntes/Programming/Socket_Programming/index.html

import socket
import struct
import time
import threading

value = 0

class MessageHandler(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client_sock, self.client_addr = client

    def run(self):

        print "got connection: {}".format(self.client_addr)
        global value

        #can use self.client_sock to call recv() and struct.unpack
        #to unpack binary structures sent to us
        self.client_sock.close()
        time.sleep(1)
