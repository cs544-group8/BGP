#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: parse_message
#Description: exposes a function for parsing raw data received by the server

import struct
from message import Message

def parse_message(raw_data):
    #pull out the header and client id first
    version, msg_type, length, reserved, clientid = struct.unpack_from('BBBBI', raw_data)

    #use the length in the header to parse the variable length payload
    payload = struct.unpack_from('%ds' % length, raw_data[8:])

    #create and return a new Message object
    msg = Message(version, msg_type, length, clientid, payload[0])
    return msg
