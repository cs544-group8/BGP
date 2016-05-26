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

class StateMachine:

    def __init__(self, client_sock, server_inst):
        self.clientsocket = client_sock
        self.server = server_inst

        self.state = IDLE

        self.version = 0x1
        self.client_id = None
        self.gametype = None

        self.msg_recvd = None

        self.opponent_sm = None

    def run_state_machine(self):
        if self.state == IDLE:
            self.printInfo("current state: Idle")
            data = self.clientsocket.recv(1024)
            if data:
                self.msg_recvd = message_parsing.parse_message(data)
                handle = self.server.msg_handler.verify_message(self.msg_recvd)
                if handle:
                    if self.msg_recvd.message_type == message.NEWGAMETYPE:
                        self.printInfo("\treceived NEWGAMETYPE going to Assign ID")
                        self.state = ASSIGN_ID
                else:
                    self.printInfo("\tmessage received was invalid, dropping")
        elif self.state == ASSIGN_ID:
            self.printInfo("current state: Assign ID")
            if self.msg_recvd:
                if game_type.game_id_check(self.msg_recvd.payload):

                    self.printInfo("\tvalid game type received: {}".format(self.msg_recvd.payload))
                    self.gametype = self.msg_recvd.payload

                    self.client_id = str(random.randint(1,256))
                    msg_to_send = message_creation.create_client_id_assign_message(self.version, self.client_id)
                    self.printMessageToSend("CLIENTIDASSIGN", msg_to_send)
                    self.clientsocket.send(msg_to_send)

                    self.printInfo("\tgoing to Find Opponent")
                    self.state = FIND_OPPONENT
                    self.msg_recvd = None
                else:
                    #invalid game type
                    self.printInfo("\tinvalid game type received: {}".format(self.msg_recvd.payload))
                    msg_to_send = message_creation.create_invalid_game_type_message(self.version)
                    self.printMessageToSend("INVALIDGAMETYPE", msg_to_send)
                    self.clientsocket.send(msg_to_send)
                    self.printInfo("going to Idle")
                    self.state = IDLE
                    self.msg_recvd = None
        elif self.state == FIND_OPPONENT:
            self.printInfo("current state: Find Opponent")
            self.printInfo("\tlooping until another client is in Find Opponent")
            self.opponent_sm = self.server.getClientInFindOpp(self.client_id)

            self.printInfo("broke out of find opp loop")
            self.printInfo("my opponents client id is: {}".format(self.opponent_sm.getClientID()))
            msg_to_send = message_creation.create_found_opponent_message(self.version, self.opponent_sm.getClientID())
            self.printMessageToSend("FOUNDOPP", msg_to_send)
            self.clientsocket.send(msg_to_send)
            self.printInfo("going to Game Start")
            self.state = GAME_START

    def printInfo(self, stmt):
        thread_name = threading.currentThread().getName()
        print "{} - client id: {}: {}".format(thread_name, self.client_id, stmt)

    def getCurrentState(self):
        return self.state

    def getClientID(self):
        return self.client_id

    def printMessageToSend(self, msg_string, msg_struct):
        self.printInfo("\tsending {}: {}".format(msg_string, message_parsing.parse_message(msg_struct)))


#current states
IDLE = 0x1
ASSIGN_ID = 0x2
FIND_OPPONENT = 0x3
GAME_START = 0x4
GAME_IN_PROGRESS = 0x5
SERVER_GAME_RESET = 0x6
GAME_END = 0x7
