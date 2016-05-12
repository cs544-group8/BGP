#!/usr/bin/python

import socket
import sys
import getopt

from messagehandler import MessageHandler

def main(argv):

    #command line args
    #-h hostname or address of the server
    #-p port to listen on
    server_name = ''
    listening_port = ''
    try:
        opts, args = getopt.getopt(argv, 'h:p:')
    except getopt.GetoptError:
        print 'main.py -h <server name> -p <port>'
        sys.exit(2)

    #parse the args
    for opt, arg in opts:
        if opt == '-h':
            server_name = arg
        elif opt == '-p':
            listening_port = int(arg)

    #bind the socker to the server address
    server_addr = (server_name, listening_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #allow the kernel to reuse sockets in TIME_WAIT state
    #prevents [Errno 98] Address already in use errors when running in
    #quick succession
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    print 'starting up on %s port %s' % server_addr
    sock.bind(server_addr)
    sock.listen(0)

    while True:
        #wait for a connection
        print 'waiting for a connection'
        client = sock.accept()
        MessageHandler(client).start()


if __name__ == "__main__":
    main(sys.argv[1:])
