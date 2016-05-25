#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message tester
#Description: Creates and parses messages in the BGP PDU format: 4x unsigned char, unsigned int, variable length char array

#to test a message: python message_tester.py
import sys
sys.path.append("../")

import random
import message_creation
import message_parsing

version = 0x1
client = random.randint(1,256)
opponent = random.randint(1,256)
move = "5"
reason = "I won"

msg = message_creation.create_invalid_game_type_message(version)
obj = message_parsing.parse_message(msg)
print "Invalid Game Type Message:"
print "\t", obj

msg = message_creation.create_client_id_assign_message(version, str(client))
obj = message_parsing.parse_message(msg)
print "Client Assign ID Message:"
print "\t", obj

msg = message_creation.create_found_opponent_message(version, str(opponent))
obj = message_parsing.parse_message(msg)
print "Found Opponent Message:"
print "\t", obj

msg = message_creation.create_game_end_message(version, reason, client)
obj = message_parsing.parse_message(msg)
print "Game End Message:"
print "\t", obj

msg = message_creation.create_game_end_ack_message(version)
obj = message_parsing.parse_message(msg)
print "Game End Ack Message:"
print "\t", obj