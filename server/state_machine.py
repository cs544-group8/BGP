#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: state_machine
#Description: defines a server state machine object and its state transitions

import message
import message_creation
import message_parsing
import game_type
import logging
import uuid
import socket
import time

class StateMachine:

    def __init__(self, version, client_sock, server_inst):
        #client socket and server instance references for convenience
        self.clientsocket = client_sock
        self.server = server_inst

        #BGP version from server
        self.version = version

        #current state of the state machine
        self.state = IDLE

        #per game attributes
        #BGP Game Type
        self.gametype = -1
        #BGP client id for game
        self.client_id = 0
        #Player number in the game
        self.player_num = -1
        #Opponent client state machine reference
        self.opponent_sm = None

        #used for states that receive a message and need to keep it around
        #for future states
        self.msg_recvd = None
        self.data = None

    # "STATEFUL" - Part the implements the DFA
    def run_state_machine(self):
        if self.state == IDLE:
            #IDLE State Handling Code
            logging.debug("Current state: Idle")
            self.gametype = -1
            self.client_id = 0
            self.player_num = -1
            self.opponent_sm = None
            if self.data:
                data = self.data
                self.data = None
            else:
                data = self.clientsocket.recv(1024)
            if data:
                self.msg_recvd = message_parsing.parse_message(data)
                if self.valid_message(self.msg_recvd):
                    if self.msg_recvd.message_type == message.NEWGAMETYPE:
                        logging.debug("received NEWGAMETYPE going to Assign ID")
                        self.state = ASSIGN_ID
                else:
                    logging.warning("message received was invalid, dropping")
            else:
                error_msg = "Socket read isn't blocking which means it was abrubtly closed by client without closing the socket"
                raise socket.error(error_msg)
        elif self.state == ASSIGN_ID:
            #ASSIGN_ID State Handling Code
            logging.debug("current state: Assign ID")
            if self.msg_recvd:
                if game_type.game_id_check(self.msg_recvd.payload):
                    #valid game type
                    logging.debug("valid game type received: {}".format(self.msg_recvd.payload))
                    self.gametype = self.msg_recvd.payload
                    #generates a random unique id that is 128 bits long - time_low gets us the first 32-bits of it - not sure if this will cause collision issues since we aren't using all 128 bits (maybe we should consider making client_id 128 bits)
                    #no need for central repository as module uuid generates ids in accordance with RFC4122
                    self.client_id = uuid.uuid4().time_low
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
            #FIND_OPPONENT State Handling Code
            logging.debug("current state: Find Opponent")
            logging.debug("looping until another client is in Find Opponent")
            #Waiting for opponent.
            while self.opponent_sm == None:
                self.server.findOpponent(self.client_id)

            logging.debug("my opponents client id is: {}".format(self.opponent_sm.getClientID()))

            msg_to_send = message_creation.create_found_opponent_message(self.version, self.client_id, self.opponent_sm.getClientID())
            self.printMessageToSend("FOUNDOPP", msg_to_send)
            self.clientsocket.send(msg_to_send)

            logging.debug("going to Game Start")
            self.state = GAME_START
        elif self.state == GAME_START:
            #GAME_START State Handling Code
            logging.debug("Current state: Game Start")
            while self.player_num == -1:
                self.server.assignPlayerNum(self.client_id)

            logging.debug("I was assigned player number {}".format(self.player_num))

            msg_to_send = message_creation.create_player_assign_message(self.version, self.client_id, self.player_num)
            self.printMessageToSend("PLAYERASSIGN", msg_to_send)
            self.clientsocket.send(msg_to_send)

            logging.debug("going to Game In Progress")
            self.state = GAME_IN_PROGRESS
        elif self.state == GAME_IN_PROGRESS:
            #GAME_IN_PROGRESS State Handling Code
            logging.debug("Current state: Game In Progress")
            if self.data:
                data = self.data
                self.data = None
            else:
                data = self.clientsocket.recv(1024)
            if data:
                msg_recvd = message_parsing.parse_message(data)
                if self.state != GAME_IN_PROGRESS:
                    self.data = data
                else:
                    if self.valid_message(msg_recvd):
                        #Forward MOVE requirement
                        if msg_recvd.message_type == message.MOVE:
                            logging.debug("received MOVE message, forwarding to opponent")
                            #message contains my client id, make new message that contains opponent's client id, so it can be forwarded
                            msg_to_send = message_creation.create_move_message(self.version, self.opponent_sm.getClientID(), msg_recvd.payload)
                            self.printMessageToSend("MOVE", msg_to_send)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                        elif msg_recvd.message_type == message.INVMOVE:
                            logging.debug("received INVMOVE message, forwarding to opponent")
                            #message contains my client id, make new message that contains opponent's client id, so it can be forwarded
                            msg_to_send = message_creation.create_invalid_move_message(self.version, self.opponent_sm.getClientID())
                            self.printMessageToSend("INVMOVE", msg_to_send)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                        elif msg_recvd.message_type == message.GAMEEND:
                            logging.debug("received GAMEEND message, forwarding to opponent")
                            #message contains my client id, make new message that contains opponent's client id so that it can be forwarded
                            msg_to_send = message_creation.create_game_end_message(self.version, msg_recvd.payload, self.opponent_sm.getClientID())
                            self.printMessageToSend("GAMEEND", msg_to_send)
                            self.opponent_sm.setCurrentState(GAME_END)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                            logging.debug("going to Game End")
                            self.state = GAME_END
                        elif msg_recvd.message_type == message.RESET:
                            logging.debug("received RESET message, forwarding to opponent")
                            #message contains my client id, make new message that contains opponent's client id so that it can be forwarded
                            msg_to_send = message_creation.create_reset_message(self.version, self.opponent_sm.getClientID())
                            self.printMessageToSend("RESET", msg_to_send)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                            logging.debug("going to Server Game Reset")
                            self.state = SERVER_GAME_RESET
                        elif msg_recvd.message_type == message.RESETACK:
                            logging.debug("received RESETACK message, forwarding to opponent")
                            msg_to_send = message_creation.create_reset_ack_message(self.version, self.opponent_sm.getClientID())
                            self.printMessageToSend("RESETACK", msg_to_send)
                            self.opponent_sm.setPlayerNum(-1)
                            self.opponent_sm.setCurrentState(GAME_START)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                            logging.debug("going to Game Start")
                            self.player_num = -1
                            self.state = GAME_START
                        elif msg_recvd.message_type == message.RESETNACK:
                            logging.debug("received RESETNACK message, forwarding to opponent")
                            msg_to_send = message_creation.create_reset_nack_message(self.version, self.opponent_sm.getClientID())
                            self.printMessageToSend("RESETNACK", msg_to_send)
                            self.opponent_sm.setCurrentState(GAME_IN_PROGRESS)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                            logging.debug("staying in Game In Progress")
                    else:
                        logging.warning("message received was invalid, dropping")
            else:
                error_msg = "Socket read isn't blocking which means it was abrubtly closed by client without closing the socket"
                raise socket.error(error_msg)
        elif self.state == SERVER_GAME_RESET:
            #SERVER_GAME_RESET State Handling Code
            logging.debug("Current state: Server Game Reset, waiting for opponent to send RESETACK or RESETNACK")
            
        elif self.state == GAME_END:
            #GAME_END State Handling Code
            logging.debug("Current state: Game End")
            if self.data:
                data = self.data
                self.data = None
            else:
                data = self.clientsocket.recv(1024)
            if data:
                msg_recvd = message_parsing.parse_message(data)
                if self.state == GAME_END:
                    if self.valid_message(msg_recvd):
                        if msg_recvd.message_type == message.GAMEENDACK:
                            logging.debug("received GAMEENDACK, forwarding to opponent")
                            #message contains my client id, make new message that contains opponent's client id so that it can be forwarded
                            msg_to_send = message_creation.create_game_end_ack_message(self.version, self.opponent_sm.getClientID())
                            self.printMessageToSend("GAMEENDACK", msg_to_send)
                            self.opponent_sm.setCurrentState(IDLE)
                            self.opponent_sm.clientsocket.send(msg_to_send)
                            logging.debug("going to Idle")
                            self.state = IDLE
                    else:
                        logging.warning("message received was invalid, dropping")
                else:
                    self.data = data
            else:
                error_msg = "Socket read isn't blocking which means it was abrubtly closed by client without closing the socket"
                raise socket.error(error_msg)
        else:
            raise Exception('Server in invalid state')

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

    #Sender Message Authentication requirement
    def valid_message(self, msg):
        if msg.version != self.version:
            return False
        elif msg.client_id != self.client_id:
            return False
        return True


#current states
IDLE = 0x1
ASSIGN_ID = 0x2
FIND_OPPONENT = 0x3
GAME_START = 0x4
GAME_IN_PROGRESS = 0x5
SERVER_GAME_RESET = 0x6
GAME_END = 0x7
