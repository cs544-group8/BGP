#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message
#Description: defines a server state machine object and its state transitions

IDLE = 0x1
ASSIGN_ID = 0x2
FIND_OPPONENT = 0x3
GAME_START = 0x4
GAME_IN_PROGRESS = 0x5
SERVER_GAME_RESET = 0x6
GAME_END = 0x7