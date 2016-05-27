#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: testclient
#Description: Hard coded client for localhost:9999 that sends messages in the BGP PDU format: 4x unsigned char, unsigned int, variable length char array

#to send a message: python testclient.py

import socket
import sys
import struct

sys.path.append("../")
import message_creation
import message
import message_parsing

HOST,PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

running = True
while running:
    try:
        line = raw_input('> ')
        if line == '1':
            msg_to_send = message_creation.create_message(1, message.NEWGAMETYPE, payload="1")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
        elif line == '6':
            msg_to_send = message_creation.create_message(1, message.MOVE, 2345, payload="placed 0 at tile 9")
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
    except socket.error:
        print "server closed connection, shutting down"
        sock.close()
        running = False
    except KeyboardInterrupt:
        print "ctrl+c detected, shutting down"
        sock.close()
        running = False