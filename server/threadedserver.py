#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: threadedserver
#Description: Starts a TCPServer on the port passed in and waits for connections.  Each connection is handled in it's own thread by the ThreadedRequestHandler class (handle() method)

#to start the server: python threadedserver.py -p <port number>

#code adapted from: https://docs.python.org/2/library/socketserver.html

import threading
import SocketServer
import getopt
import sys
import message_parsing
from message_handler import MessageHandler

class ThreadedRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        print '{} handling message sent from: {}'.format(cur_thread.getName(), self.client_address)

        msg_recvd = message_parsing.parse_message(data)
        print "new message parsed: {}".format(msg_recvd)
        #self.server refers to the ThreadedServer object which comes as part of this object when we 
        #get a request
        handle_msg = self.server.msg_handler.verify_message(msg_recvd)

        if handle_msg:
            print "new message verified, handing to state machine"
            #pass message to state machine here
        else:
            print "new message is not valid, dropping"

        return

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    #allow ctrl-c to kill all spawned threads
    daemon_threads = True
    #eliminates a port rebinding error when you repeatedly start/stop the server in quick succession
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        #instantiate message handler to be used in the ThreadedRequestHandler
        self.msg_handler = MessageHandler(1)
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

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

    server = ThreadedServer(('', port), ThreadedRequestHandler)
    ip, port = server.server_address
    print 'Server running at {} on port {}'.format(ip, port)

    #start it up, catch ctrl+c to end the server loop and clean-up
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "\nShutting down server loop and cleaning up"
        server.shutdown()
        server.server_close()
