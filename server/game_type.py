#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: game_type
#Description: defines valid game types and exposes a method to check if a game type id is valid

#Game Type Validation requirement
def game_id_check(game_type_id):
    if game_type_id in [TICTACTOE]:
        return True
    else:
        return False

TICTACTOE = "1"
