#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: game_type
#Description: defines valid game types and exposes a method to check if a game type id is valid

def game_id_check(game_type_id):
    if game_type_id in ["1"]:
        return True
    else:
        return False
