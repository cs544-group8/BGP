#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message tester
#Description: Creates and parses messages in the BGP PDU format: 4x unsigned char, unsigned int, variable length char array

#to send a message: python message_tester.py

import random
import message_creation
import message_parsing

version = 0x1
client = hex(random.randint(1,256))
opponent = hex(random.randint(1,256))
move = "5"
reason = "I won"

msg1 = message_creation.create_valid_game_type_message(version)
obj1 = message_parsing.parse_message(msg1)
print "Valid Valid Game Message:"
print "\t", obj1

msg2 = message_creation.create_invalid_game_type_message(version)
obj2 = message_parsing.parse_message(msg2)
print "Valid Invalid Game Message:"
print "\t", obj2

msg3 = message_creation.create_client_id_assignment_message(version, str(client))
obj3 = message_parsing.parse_message(msg3)
print "Valid Client ID Message:"
print "\t", obj3

msg4 = message_creation.create_wait_for_opponent_message(version)
obj4 = message_parsing.parse_message(msg4)
print "Valid Wait for Opponent Message:"
print "\t", obj4

msg5 = message_creation.create_found_opponent_message(version, str(opponent))
obj5 = message_parsing.parse_message(msg5)
print "Valid Found Opponent Message:"
print "\t", obj5

msg6 = message_creation.create_reqmove_opponent_message(version, client, str(opponent) )
obj6 = message_parsing.parse_message(msg6)
print "Valid Request Move Message:"
print "\t", obj6


msg7 = message_creation.create_opponent_move_message(version, client, move)
obj7 = message_parsing.parse_message(msg7)
print "Valid Opponent Move Message:"
print "\t", obj7

msg8 = message_creation.create_game_end_message(version, reason, client)
obj8 = message_parsing.parse_message(msg8)
print "Valid Game End Message:"
print "\t", obj8

msg9 = message_creation.create_game_end_ack_message(version)
obj9 = message_parsing.parse_message(msg9)
print "Valid Game End Ack Message:"
print "\t", obj9