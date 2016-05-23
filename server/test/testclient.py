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
import binascii

sys.path.append("../")
import message_creation

HOST,PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST,PORT))
    # msg_to_send = message_creation.create_opponent_move_message(1, 12345, "hello")
    sock.sendall(msg_to_send)
finally:
    sock.close()

print "Sent ({} bytes): {}".format(len(msg_to_send),
    binascii.hexlify(msg_to_send))
