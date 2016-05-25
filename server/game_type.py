#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message
#Description: defines valid game types

def game_id_check(game_id):
    if game_id in ["1","2","3"]:
        return True
    else:
        return False