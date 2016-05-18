# This module is created to create Messages

import struct

def parse_message(message):
    '''The function breaks up message into:
    version
    message type
    payload
    client id
    Input:
        Message
    Output:
        Message Class Object
    '''
    # message parsing and class istantiation.
    # planning on using struct python module for parsing
    return msg_obj