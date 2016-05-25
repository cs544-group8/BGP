#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message tester
#Description: Creates and send messages through the state_machine

#to send a message: python message_tester.py

import random
import message_creation
import message_parsing
import state_machine
from message import VALGAMETYPE,NEWGAMETYPE,INVGAMETYPE,CLIENTIDASSIGN,FINDOPP,WAITFOROPP,FOUNDOPP,REQMOVE,MOVE,OPPMOVE,GAMEEND,GAMEENDACK

version = 0x1
client = random.randint(1,256)
opponent = random.randint(1,256)

server_state_machine = state_machine.ServerStateMachine(version)

print 1
msg = message_creation.create_game_end_message(version, "Don't want to play", 0)
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 2
server_state_machine.handle_message(None)

print 3
msg = message_creation.create_message(version, NEWGAMETYPE, payload="10")
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 4
msg = message_creation.create_message(version, NEWGAMETYPE, payload="1")
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 5
server_state_machine.handle_message(None)

print 6
msg = message_creation.create_message(version, FINDOPP)
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 7
server_state_machine.handle_message(None)

print 8
msg = message_creation.create_reqmove_opponent_message(version, client, str(opponent) )
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 9
server_state_machine.handle_message(None)

print 10
server_state_machine.handle_message(None)

print 11
msg = message_creation.create_message(version, MOVE, client_id=opponent, payload="5")
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)

print 12
msg = message_creation.create_message(version, MOVE, client_id=opponent, payload="5")
msg_obj = message_parsing.parse_message(msg)
server_state_machine.handle_message(msg_obj)