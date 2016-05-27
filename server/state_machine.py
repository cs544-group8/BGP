#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message
#Description: defines a server state machine object and its state transitions

import message
import message_creation
import message_parsing
import random
import game_type
import threading
import logging

class StateMachine:

    def __init__(self, client_sock, server_inst):
        self.clientsocket = client_sock
        self.server = server_inst

        self.state = IDLE

        self.version = 0x1
        self.client_id = 0
        self.gametype = None

        self.msg_recvd = None

        self.opponent_sm = None

        self.player_num = -1

    def run_state_machine(self):
        if self.state == IDLE:
            logging.debug("Current state: Idle")
            data = self.clientsocket.recv(1024)
            if data:
                self.msg_recvd = message_parsing.parse_message(data)
                handle = self.server.msg_handler.verify_message(self.msg_recvd)
                if handle:
                    if self.msg_recvd.message_type == message.NEWGAMETYPE:
                        logging.debug("received NEWGAMETYPE going to Assign ID")
                        self.state = ASSIGN_ID
                else:
                    logging.debug("message received was invalid, dropping")
        elif self.state == ASSIGN_ID:
            logging.debug("current state: Assign ID")
            if self.msg_recvd:
                if game_type.game_id_check(self.msg_recvd.payload):

                    logging.debug("valid game type received: {}".format(self.msg_recvd.payload))
                    self.gametype = self.msg_recvd.payload

                    self.client_id = random.randint(1,256)
                    msg_to_send = message_creation.create_client_id_assign_message(self.version, self.client_id)
                    self.printMessageToSend("CLIENTIDASSIGN", msg_to_send)
                    self.clientsocket.send(msg_to_send)

                    logging.debug("going to Find Opponent")
                    self.state = FIND_OPPONENT
                    self.msg_recvd = None
                else:
                    #invalid game type
                    logging.debug("invalid game type received: {}".format(self.msg_recvd.payload))
                    msg_to_send = message_creation.create_invalid_game_type_message(self.version)
                    self.printMessageToSend("INVALIDGAMETYPE", msg_to_send)
                    self.clientsocket.send(msg_to_send)
                    logging.debug("going to Idle")
                    self.state = IDLE
                    self.msg_recvd = None
        elif self.state == FIND_OPPONENT:
            logging.debug("current state: Find Opponent")
            logging.debug("looping until another client is in Find Opponent")
            while self.opponent_sm == None:
                self.server.findOpponent(self.client_id)

            logging.debug("my opponents client id is: {}".format(self.opponent_sm.getClientID()))

            msg_to_send = message_creation.create_found_opponent_message(self.version, self.opponent_sm.getClientID())
            self.printMessageToSend("FOUNDOPP", msg_to_send)
            self.clientsocket.send(msg_to_send)

            logging.debug("going to Game Start")
            self.state = GAME_START
        elif self.state == GAME_START:
            logging.debug("Current state: Game Start")
            while self.player_num == -1:
                self.server.assignPlayerNum(self.client_id)

            logging.debug("I was assigned player number {}".format(self.player_num))
            #send to client
            msg_to_send = message_creation.create_player_assign_message(self.version, self.client_id, self.player_num)
            self.printMessageToSend("PLAYERASSIGN", msg_to_send)
            self.clientsocket.send(msg_to_send)

            logging.debug("going to Game In Progress")
            self.state = GAME_IN_PROGRESS

    def setPlayerNum(self, p_id):
        self.player_num = p_id

    def getPlayerNum(self):
        return self.player_num

    def setCurrentState(self, new_state):
        self.state = new_state

    def getCurrentState(self):
        return self.state

    def setOpponent(self, opp):
        self.opponent_sm = opp

    def getClientID(self):
        return self.client_id

    def printMessageToSend(self, msg_string, msg_struct):
        logging.debug("sending {}: {}".format(msg_string, message_parsing.parse_message(msg_struct)))


#current states
IDLE = 0x1
ASSIGN_ID = 0x2
FIND_OPPONENT = 0x3
GAME_START = 0x4
GAME_IN_PROGRESS = 0x5
SERVER_GAME_RESET = 0x6
GAME_END = 0x7
