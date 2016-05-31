#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message_creation
#Description: exposes functions to create various message types

import struct
import message

#base function for creating a message, called by the more specific create* functions below
def create_message(version, msg_type, client_id=None, payload=None):
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
    reserved = 0x0

    if payload == None:
        payload = ""
    length = len(payload)

    if client_id == None:
        client_id = 0

    s = struct.Struct('BBBBI%ds' % length)
    message_data = (version, msg_type, length, reserved, client_id, payload)
    message = s.pack(*message_data)

    return message

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
    return create_message(version, message.INVGAMETYPE)

# Create CLIENTIDASSIGN Message
def create_client_id_assign_message(version, client_id):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version and client id payload.
    It also adds CLIENTIDASSIGN message type for message creation

    Input:
        Version: Protocol Version
        Payload: ID assigned to receipient client
    Output:
        Message: return from create_message
    '''
    return create_message(version, message.CLIENTIDASSIGN, payload=str(client_id))

# Create FOUNDOPP Message
def create_found_opponent_message(version, client_id, opponent_ID):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version and opponent client id payload.
    It also adds FOUNDOPP message type for message creation

    Input:
        Version: Protocol Version
        Payload: Opponet client ID
    Output:
        Message: return from create_message
    '''
    return create_message(version, message.FOUNDOPP, client_id = int(client_id), payload=str(opponent_ID))

# Create PLAYERASSIGN Message
def create_player_assign_message(version, client_id, player_id):
    '''The function is used to create a player assign message.
    This function passes through protocol version and player assigned id payload.
    It also adds PLAYERASSIGN message type for message creation

    Input:
        Version: Protocol Version
        Payload: Player Assigned ID
    Output:
        Message: return from create_message
    '''
    return create_message(version, message.PLAYERASSIGN, client_id=int(client_id), payload=str(player_id))

#create MOVE message
def create_move_message(version, client_id, move_data):
    return create_message(version, message.MOVE, client_id=int(client_id), payload=str(move_data))

def create_invalid_move_message(version, client_id):
    return create_message(version, message.INVMOVE, client_id=int(client_id))

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
    return create_message(version, message.GAMEEND, client_id=int(client_id), payload=reason)

# Create GAMEENDACK Message
def create_game_end_ack_message(version, client_id):
    '''The function is used to create a client id assignment message.
    This function passes through protocol version.
    It also adds GAMEENDACK message type for message creation

    Input:
        Version: Protocol Version
        Payload: ID assigned to receipient client
    Output:
        Message: return from create_message
    '''
    return create_message(version, message.GAMEENDACK, client_id=int(client_id))

def create_reset_message(version, client_id):
    return create_message(version, message.RESET, client_id=int(client_id))

def create_reset_ack_message(version, client_id):
    return create_message(version, message.RESETACK, client_id=int(client_id))

def create_reset_nack_message(version, client_id):
    return create_message(version, message.RESETNACK, client_id=int(client_id))
