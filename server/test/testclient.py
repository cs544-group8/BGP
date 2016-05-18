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
from ctypes import *
import binascii

HOST,PORT = "localhost", 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST,PORT))
    payload = 'test message'
    values = (1, 10, len(payload), 0, 12345, payload)

    #BBBBI*s --> 4 unsigned chars, unsigned int, char []
    s = struct.Struct('BBBBI%ds' % len(payload))
    packed_data = s.pack(*values)
    sock.sendall(packed_data)
finally:
    sock.close()

print "Sent ({} bytes): {}".format(s.size,
    binascii.hexlify(packed_data))
