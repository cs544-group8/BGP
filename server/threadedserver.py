#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: threadedserver
#Description: Starts a TCPServer on the port passed in and waits for connections.  Each connection is handled in it's own thread by the ThreadedRequestHandler class (handle() method)

#to start the server: python threadedserver.py (listens on port 9999)

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
        logging.info("Handling connection from: {}".format(self.client_address))

        statemachine = state_machine.StateMachine(self.server.version, self.request, self.server)
        self.server.addStateMachineToList(statemachine)

        while True:
            try:
                statemachine.run_state_machine()
            except Exception as e_inst:
                logging.error("Exception occured: {}".format(e_inst))
                self.request.close()
                return False
        return

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    #allow ctrl-c to kill all spawned threads
    daemon_threads = True
    #eliminates a port rebinding error when you repeatedly start/stop the server in quick succession
    allow_reuse_address = True
    #hard coded version to be used throughout the protocol
    version = 0x1

    def __init__(self, server_address, RequestHandlerClass):
        self.lock = threading.RLock()
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
    logging.info('Server running at {} on port {} using BGP v{}'.format(ip, port, server.version))

    #start it up, catch ctrl+c to end the server loop and clean-up
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server loop and cleaning up")
        server.shutdown()
        server.server_close()
