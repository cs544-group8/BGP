#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: threadedserver
#Description: Starts a TCPServer on the port passed in and waits for connections.  Each connection is handled in it's own thread by the ThreadedRequestHandler class (handle() method)

#to start the server: python threadedserver.py -p <port number>

#code adapted from: https://docs.python.org/2/library/socketserver.html

import threading
import SocketServer
import logging
import getopt
import sys
import random
import message_parsing
import message_creation
import message_handler
import state_machine
import message
import game_type

class ThreadedRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        logging.debug("Handling connection from: {}".format(self.client_address))

        statemachine = state_machine.StateMachine(self.request, self.server)
        self.server.addStateMachineToList(statemachine)

        while True:
            try:
                statemachine.run_state_machine()
            except Exception as e_inst:
                logging.error("Exception occured: {}".format(e_inst))
                self.request.close()
                return False

        # state = state_machine.IDLE
        # version = 0x1
        # msg_recvd = None
        # opponent = None
        # client_id = None
        # client_GE = True
        # client_RS = True
        # while True:
        #     try:
        #         print "Current State:"+str(state)
        #         if state == state_machine.IDLE:
        #             data = self.request.recv(1024)
        #             if data:
        #                 msg_recvd = message_parsing.parse_message(data)
        #                 if self.server.msg_handler.verify_message(msg_recvd):
        #                     if msg_recvd.message_type == message.NEWGAMETYPE:
        #                         state = state_machine.ASSIGN_ID
        #             else:
        #                 print "\tRecv got no data"
        #         elif state == state_machine.ASSIGN_ID:
        #             if msg_recvd:
        #                 if game_type.game_id_check(msg_recvd.payload):
        #                     client_id = random.randint(1,256)
        #                     send_msg = message_creation.create_client_id_assign_message(version, str(client_id))
        #                     state = state_machine.FIND_OPPONENT
        #                     print "\tNeed to send back to client"
        #                     print "sending {}".format(message_parsing.parse_message(send_msg))
        #                 else:
        #                     send_msg = message_creation.create_invalid_game_type_message(version)
        #                     state = state_machine.IDLE
        #                     print "\tNeed to send back to client"
        #                     print "\t", message_parsing.parse_message(send_msg)
        #         elif state == state_machine.FIND_OPPONENT:
        #             # This needs to find opponent.
        #             found_opponent = True
        #             opponent = random.randint(1,256)
        #             if opponent:
        #                 send_msg = message_creation.create_found_opponent_message(version, str(opponent))
        #                 state = state_machine.GAME_START
        #                 print "\tNeed to send back to client"
        #                 print "\t", message_parsing.parse_message(send_msg)
        #         elif state == state_machine.GAME_START:
        #             send_msg = message_creation.create_player_assign_message(version, client_id, "1")
        #             state = state_machine.GAME_IN_PROGRESS
        #             print "Need to send back to client"
        #             print "\t", message_parsing.parse_message(send_msg)
        #         elif state == state_machine.GAME_IN_PROGRESS:
        #             data = self.request.recv(1024)
        #             if data:
        #                 msg_recvd = message_parsing.parse_message(data)
        #                 if self.server.msg_handler.verify_message(msg_recvd):
        #                     if msg_recvd.message_type == message.MOVE:
        #                         print "Forward to Opponent"
        #                     elif msg_recvd.message_type == message.INVMOVE:
        #                         print "Forward to Opponent"
        #                     elif msg_recvd.message_type == message.GAMEEND:
        #                         print "Forward to Opponent"
        #                         client_GE = True
        #                         state = state_machine.GAME_END
        #                     elif msg_recvd.message_type == message.RESET:
        #                         print "Forward to Opponent"
        #                         state = state_machine.SERVER_GAME_RESET
        #             else:
        #                 print "Recv got no data"
        #         elif state == state_machine.SERVER_GAME_RESET:
        #             if client_RS:
        #                 send_msg = message_creation.create_game_end_ack_message(version)
        #                 state = state_machine.IDLE
        #                 print "Need to send back to client"
        #                 print "\t", message_parsing.parse_message(send_msg)
        #             else:
        #                 data = self.request.recv(1024)
        #                 if data:
        #                     msg_recvd = message_parsing.parse_message(data)
        #                     if self.server.msg_handler.verify_message(msg_recvd):
        #                         if msg_recvd.message_type == message.RESETACK:
        #                             print "Forward to Opponent"
        #                             state = state_machine.GAME_START
        #                         elif msg_recvd.message_type == message.RESETNACK:
        #                             print "Forward to Opponent"
        #                             state = state_machine.GAME_IN_PROGRESS
        #         elif state == state_machine.GAME_END:
        #             if client_GE:
        #                 send_msg = message_creation.create_game_end_ack_message(version)
        #                 state = state_machine.IDLE
        #                 print "Need to send back to client"
        #                 print "\t", message_parsing.parse_message(send_msg)
        #             else:
        #                 data = self.request.recv(1024)
        #                 if data:
        #                     msg_recvd = message_parsing.parse_message(data)
        #                     if self.server.msg_handler.verify_message(msg_recvd):
        #                         if msg_recvd.message_type == message.GAMEENDACK:
        #                             state = state_machine.IDLE
        #         else:
        #             raise Exception('Server in invalide state')
        #     except Exception as e_inst:
        #         print "Exception: ", e_inst
        #         self.request.close()
        #         return False;

        return

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    #allow ctrl-c to kill all spawned threads
    daemon_threads = True
    #eliminates a port rebinding error when you repeatedly start/stop the server in quick succession
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        self.lock = threading.RLock()
        self.msg_handler = message_handler.MessageHandler(1)
        self.state_machines = []
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

    def addStateMachineToList(self, sm):
        self.lock.acquire()
        self.state_machines.append(sm)
        self.lock.release()

    #thread safe function that matches two client's that are both in Find Opponent state
    def findOpponent(self, client_id):

        #get a reference to the state machine that called this function
        calling_sm = self.getStateMachineByClientID(client_id)
        self.lock.acquire()
        #now search for an opponent
        viable_opponent = None
        for sm in self.state_machines:
            if(sm.getCurrentState() == state_machine.FIND_OPPONENT and sm.getClientID() != client_id):
                if calling_sm.opponent_sm == None:
                    calling_sm.setOpponent(sm)
                    sm.setOpponent(calling_sm)
                    break
        self.lock.release()

    #helper function to get a state machine object from the list by client_id
    def getStateMachineByClientID(self, client_id):
        target_sm = None
        self.lock.acquire()
        for sm in self.state_machines:
            if(sm.getClientID() == client_id):
                target_sm = sm
                break
        self.lock.release()
        return target_sm

    #thread safe function to assign a state machine (and it's opponent) a player number
    def assignPlayerNum(self, client_id):
        sm_to_set = self.getStateMachineByClientID(client_id)
        self.lock.acquire()
        if sm_to_set.getPlayerNum() == -1:
            sm_to_set.setPlayerNum(1)
            sm_to_set.opponent_sm.setPlayerNum(2)
        self.lock.release()


if __name__ == '__main__':

    #configure logging so we have thread names in our print statements automatically
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:(%(threadName)s) - %(message)s')

    port = 9999

    server = ThreadedServer(('', port), ThreadedRequestHandler)
    ip, port = server.server_address
    logging.info('Server running at {} on port {}'.format(ip, port))

    #start it up, catch ctrl+c to end the server loop and clean-up
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server loop and cleaning up")
        server.shutdown()
        server.server_close()
