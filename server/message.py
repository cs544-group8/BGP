#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message
#Description: defines a Message object to be used throughout the server - raw data will be parsed and instantiated into an object where the fields of a message are easy to access

class Message(object):
    '''
    Class used to represent a sturcture of the data contained in a message
    '''
    def __init__(self, version, message_type, length, client_id=None, payload=None,):
        '''
        Intialization function of message class object.
        Input:
            Version: Message Version, required for all messages
            Message Type: Message Type, required for all messages
            Payload: Payload contained in the data, not required for all messages
            Client ID: ID associated in message, not required for all messages
        '''
        self.version = version
        self.message_type = message_type
        self.length = length
        self.payload = payload
        self.client_id = client_id

    def __repr__(self):
        return "Version: {}, Msg Type: {}, Length: {}, ClientID: {}, Payload: {}".format(self.version, self.message_type, self.length, self.client_id, self.payload)

VALGAMETYPE     = 0x9
NEWGMETYPE      = 0xa
INVGAMETYPE     = 0xb
CLIENTIDASSIGN  = 0xc
FINDOPP         = 0xd
WAITFOROPP      = 0xe
FOUNDOPP        = 0xf
REQMOVE         = 0x14
MOVE            = 0x15
OPPMOVE         = 0x16
GAMEEND         = 0x17
GAMEENDACK      = 0x18