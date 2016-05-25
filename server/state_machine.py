#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message
#Description: defines a server state machine object and its state transitions

from message import VALGAMETYPE,NEWGAMETYPE,INVGAMETYPE,CLIENTIDASSIGN,FINDOPP,WAITFOROPP,FOUNDOPP,REQMOVE,MOVE,OPPMOVE,GAMEEND,GAMEENDACK
import game_type
import message_creation
import message_parsing
import random

IDLE = 0x1
GAME_TYPE_ESTABLISHED = 0x2
CLIENT_ID_ASSIGNED = 0x3
FINDING_OPPONENT = 0x4
GAME_IN_PROGRESS = 0x5
MOVE_REQUEST_RECEIVED = 0x6
MOVE_REQUEST_SENT = 0x7
WAITING_FOR_MOVE = 0x8
FORWARD_MOVE = 0x9
GAME_END_RECEIVED = 0xA
GAME_END_SENT = 0xB

class ServerStateMachine(object):
    '''
    Class used to represent the state of a server client connection
    '''
    def __init__(self, version):
        '''
        Intialization function of Server State Machine Class.
        Input:
        '''
        self.version = version
        self.state = IDLE
        self.partner_machine = None
        self.client_id = None
    
    def handle_message(self, msg):
        if self.state == IDLE:
            print "Idle State"
            if msg.message_type == NEWGAMETYPE:
                # Checking Game type is valid.
                if game_type.game_id_check(msg.payload):
                    #valid game
                    print "\tReceived valid NEWGAMETYPE("+str(NEWGAMETYPE)+"), type="+msg.payload
                    new_msg = message_creation.create_valid_game_type_message(self.version)
                    print "\tSend:", message_parsing.parse_message(new_msg)
                    self.state = GAME_TYPE_ESTABLISHED
                    print "\tSent VALGAMETYPE("+str(VALGAMETYPE)+") goto GAME_TYPE_ESTABLISHED"
                else:
                    #invalid game
                    print "\tReceived invalid NEWGAMETYPE("+str(NEWGAMETYPE)+"), type="+msg.payload
                    new_msg = message_creation.create_invalid_game_type_message(self.version)
                    print "\tSend:", message_parsing.parse_message(new_msg)
                    print "\tSent INVGAMETYPE("+str(INVGAMETYPE)+") stay in IDLE"
            elif msg.message_type == GAMEEND:
                self.state = GAME_END_RECEIVED
                print "\tReceived GAMEEND("+str(GAMEEND)+") goto GAME_END_RECEIVED"
            else:
                # Do we want to throw and invalide message back or something?
                print "\tReceived unexpected message drop it"
                print "\tDroping", message_parsing.parse_message(msg)
                return
        elif self.state == GAME_TYPE_ESTABLISHED:
            print "Game Type Established State"
            self.client_id = random.randint(1,256)
            new_msg = message_creation.create_client_id_assignment_message(self.version, str(self.client_id))
            print "\tSend:", message_parsing.parse_message(new_msg)
            self.state = CLIENT_ID_ASSIGNED
            print "\tSent CLIENTIDASSIGN("+str(CLIENTIDASSIGN)+") goto CLIENT_ID_ASSIGNED"
        elif self.state == CLIENT_ID_ASSIGNED:
            print "Client ID Assigned State"
            if msg.message_type == FINDOPP:
                print "\tWaiting for other thread to need opponent"
                self.state = FINDING_OPPONENT
                print "\tReceived FINDOPP("+str(FINDOPP)+") goto FINDING_OPPONENT"
            elif msg.message_type == GAMEEND:
                self.state = GAME_END_RECEIVED
                print "\tReceived GAMEEND("+str(GAMEEND)+") goto GAME_END_RECEIVED"
            else:
                # Do we want to throw and invalide message back or something?
                print "\tReceived unexpected message drop it"
                print "\tDroping", message_parsing.parse_message(msg)
                return
        elif self.state == FINDING_OPPONENT:
            print "Finding Opponent State"
            print "\tOpponent found"
            opponent = random.randint(1,256)
            new_msg = message_creation.create_found_opponent_message(self.version, str(opponent))
            print "\tSend:", message_parsing.parse_message(new_msg)
            self.state = GAME_IN_PROGRESS
            print "\tSent FOUNDOPPONENT("+str(FOUNDOPP)+") goto GAME_IN_PROGRESS"
        elif self.state == GAME_IN_PROGRESS:
            print "Game In Progress State"
            if msg.message_type == REQMOVE:
                self.state = MOVE_REQUEST_RECEIVED
                print "\tReceived REQMOVE("+str(REQMOVE)+") goto MOVE_REQUEST_RECEIVED"
            else:
                # Do we want to throw and invalide message back or something?
                print "\tReceived unexpected message drop it"
                print "\tDroping", message_parsing.parse_message(msg)
                return
        elif self.state == MOVE_REQUEST_RECEIVED:
            print "Move Request Received State"
            opponent = random.randint(1,256)
            new_msg = message_creation.create_reqmove_opponent_message(self.version, self.client_id, str(opponent) )
            print "\tSend:", message_parsing.parse_message(new_msg)
            self.state = MOVE_REQUEST_SENT
            print "\tSent REQMOVE("+str(REQMOVE)+") goto MOVE_REQUEST_SENT"
        elif self.state == MOVE_REQUEST_SENT:
            print "Move Requst Sent State"
            new_msg = message_creation.create_wait_for_opponent_message(self.version)
            print "\tSend:", message_parsing.parse_message(new_msg)
            self.state = WAITING_FOR_MOVE
            print "\tSent WAITFOROPP("+str(WAITFOROPP)+") goto WAITING_FOR_MOVE"
        elif self.state == WAITING_FOR_MOVE:
            print "Waiting For Move State"
            if msg.message_type == MOVE:
                self.state = FORWARD_MOVE
                print "\tReceived MOVE("+str(MOVE)+") goto FORWARD_MOVE"
            elif msg.message_type == GAMEEND:
                self.state = GAME_END_RECEIVED
                print "\tReceived GAMEEND("+str(GAMEEND)+") goto GAME_END_RECEIVED"
            else:
                # Do we want to throw and invalide message back or something?
                print "\tReceived unexpected message drop it"
                print "\tDroping", message_parsing.parse_message(msg)
                return
        elif self.state == FORWARD_MOVE:
            print "Forward Move State"
            new_msg = message_creation.create_opponent_move_message(self.version, msg.client_id, msg.payload)
            print "\tSend:", message_parsing.parse_message(new_msg)
            print "\tSent OPPMOVE("+str(OPPMOVE)+") goto GAME_IN_PROGRESS"
        elif self.state == GAME_END_RECEIVED:
            print "Game End Received State"
            new_msg = message_creation.create_game_end_ack_message(self.version)
            print "\tSend:", message_parsing.parse_message(new_msg)
            if self.partner_machine != None:
                print "\tTell partner thread to send GAMEEND message"
            print "\tSent GAMEENDACK("+str(GAMEENDACK)+") goto IDLE"
            self.state = IDLE
        elif self.state == GAME_END_SENT:
            print "Game End Sent State"
            if msg.message_type == GAMEENDACK:
                print "\tReceived GAMEENDACK("+str(GAMEENDACK)+") goto IDLE"
                self.state = IDLE
            else:
                # Do we want to throw and invalide message back or something?
                print "\tReceived unexpected message drop it"
                print "\tDroping", message_parsing.parse_message(msg)
                return
        else:
            print "Server in unknown state"