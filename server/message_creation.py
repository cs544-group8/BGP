#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message_creation
#Description: exposes functions to create various message types

import struct
from message import VALGAMETYPE, INVGAMETYPE, CLIENTIDASSIGN, WAITFOROPP, FOUNDOPP, REQMOVE, OPPMOVE, GAMEEND, GAMEENDACK

def create_message(version, msg_type, payload=None, client_id=None):
    '''The function is used to create a message.
    Input:
        Version: Protocol Version
        Message Type: Protocol Message Type
        Payload: Payload of message, Varies depending on Message
            Used to derive Length
        Clien ID: ID of client, Varies depending on Message
    Output:
        Message: Constructed message to send
    '''
    # Message Creation code here
    # planning on using struct python module for parsing
    reserved = 0x0
    
    if payload == None:
        payload = ""
    length = len(payload)
    
    if client_id == None:
        client_id = 0

    message = struct.pack('BBBBI%ds' % length, version, msg_type, length, client_id, reserved, payload)
    return message

# Server doesn't need to create NEWGAMETYPE Message

# This Message Type doesn't exist Should add
def create_valid_game_type_message(version):
    '''The function is used to create a valid game type message.
    This function passes through protocol version and
    adds VALGAMETYPE message type for message creation

    Input:
        Version: Protocol Version
    Output:
        Message: return from create_message
    '''
    return create_message(version, VALGAMETYPE)


# Create INVGAMETYPE Message
def create_invalid_game_type_message(version):
    '''The function is used to create a invalid game type message.
    This function passes through protocol version and
    adds INVGAMETYPE message type for message creation

    Input:
        Version: Protocol Version
    Output:
        Message: return from create_message
    '''
    return create_message(version, INVGAMETYPE)

# Create CLIENTIDASSIGN Message
def create_client_id_assignment_message(version, client_id):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version and client id payload.
    It also adds CLIENTIDASSIGN message type for message creation

    Input:
        Version: Protocol Version
        Payload: ID assigned to receipient client
    Output:
        Message: return from create_message
    '''
    return create_message(version, CLIENTIDASSIGN, payload=client_id)

# Server doesn't need to create FINDOPP Message

# Create WAITFOROPP Message
def create_wait_for_opponent_message(version):
    '''The function is used to create wait for opponent message.
    This function passes through protocol version and
    also adds WAITFOROPP message type for message creation

    Input:
        Version: Protocol Version
    Output:
        Message: return from create_message
    '''
    return create_message(version, WAITFOROPP)

# Create FOUNDOPP Message
def create_found_opponent_message(version, opponent_ID):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version and opponent client id payload.
    It also adds FOUNDOPP message type for message creation

    Input:
        Version: Protocol Version
        Payload: Opponet client ID
    Output:
        Message: return from create_message
    '''
    return create_message(version, FOUNDOPP, payload=opponent_ID)

# Create REQMOVE Message
def create_reqmove_opponent_message(version, requester_id, requestie_id ):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version, requester client id,
    and requestie client id payload.
    It also adds REQMOVE message type for message creation

    Input:
        Version: Protocol Version
        Client ID: ID of requesting client
        Payload: ID of requested client
    Output:
        Message: return from create_message
    '''
    return create_message(version, REQMOVE, client_id=requester_id, payload=requestie_id)

# Server doesn't need to create FINDOPP Message

# Create OPPMOVE Message
def create_opponent_move_message(version, client_id, move):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version, opponent client id,
    and move data payload.
    It also adds OPPMOVE message type for message creation

    Input:
        Version: Protocol Version
        Client ID: Client ID of opponent
        Payload: Move data
    Output:
        Message: return from create_message
    '''
    return create_message(version, OPPMOVE, client_id=client_id, payload=move)

# Create GAMEEND Message
def create_game_end_message(version, reason, client_id):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version, client id of originator,
    and reason payload.
    It also adds GAMEEND message type for message creation

    Input:
        Version: Protocol Version
        Client ID: ID of Originator of Game End messge
        Payload: Reason of end game
    Output:
        Message: return from create_message
    '''
    return create_message(version, GAMEEND, client_id=client_id, payload=reason)

# Create GAMEENDACK Message
def create_game_end_ack_message(version):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version.
    It also adds GAMEENDACK message type for message creation

    Input:
        Version: Protocol Version
        Payload: ID assigned to receipient client
    Output:
        Message: return from create_message
    '''
    return create_message(version, GAMEENDACK)
