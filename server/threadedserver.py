#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: threadedserver
#Basic Description: Starts a TCPServer on the port passed in and waits for connections.  Each connection is handled in it's own thread by the ThreadRequestHandler class (handle() method)

#to start the server: python threadedserver.py -p <port number>

#code adapted from: https://docs.python.org/2/library/socketserver.html

import threading
import SocketServer
import getopt
import sys

class ThreadedRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        cur_thread = threading.currentThread()

        #prints the current thread name, the client who sent the data, and the data itself
        print 'Handled in {}, {} sent: \n{}'.format(cur_thread.getName(), self.client_address, self.data)
        return

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    argv = sys.argv[1:]

    port = ''

    try:
        opts, args = getopt.getopt(argv, 'h:p:')
    except getopt.GetoptError:
        print 'threadedserver.py -p <port>'
        sys.exit(2)

    #parse the arg(s)
    for opt, arg in opts:
        if opt == '-p':
            port = int(arg)

    #eliminates an error thrown if you repeatedly start and stop the server in quick succession
    ThreadedServer.allow_reuse_address = True
    server = ThreadedServer(('localhost', port), ThreadedRequestHandler)
    ip, port = server.server_address
    print 'Server running at {} on port {}'.format(ip, port)

    #start it up, catch ctrl+c to end the server loop and clean-up
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "\nShutting down server loop and cleaning up"
        server.shutdown()
        server.server_close()
