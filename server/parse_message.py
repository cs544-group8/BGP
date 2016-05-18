#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: parse_message
#Description: exposes an object for holding messages and a function for parsing raw data received by the server

import struct
import binascii

class Message:

    def __init__(self, data):
        self.version = data[0]
        self.msg_type = data[1]
        self.length = data[2]
        self.clientid = data[3]
        self.payload = data[4]

    def __repr__(self):
        return "Version: {}, Msg Type: {}, Length: {}, ClientID: {}, Payload: {}".format(self.version, self.msg_type, self.length, self.clientid, self.payload)

def parse_message(raw_data):
    #pull out the header and client id first
    version, msg_type, length, reserved, clientid = struct.unpack_from('BBBBi', raw_data)

    #use the length in the header to parse the variable length payload
    payload = struct.unpack_from('%ds' % length, raw_data[8:])

    #create and return a new Message object
    msg = Message([version, msg_type, length, clientid, payload[0]])
    return msg
