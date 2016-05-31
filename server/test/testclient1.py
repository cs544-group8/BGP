#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: testclient1
#Description: Hard coded client for localhost:9999 that sends messages in the BGP PDU format: 4x unsigned char, unsigned int, variable length char array

#to send a message: python testclient.py

import socket
import sys

sys.path.append("../")
import message_creation
import message_parsing
import message

HOST,PORT = "localhost", 9999
client_id = None
test_twice = True
test_reset = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST,PORT))

    msg_to_send = message_creation.create_message(1, message.NEWGAMETYPE, payload="1")
    print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
    sock.send(msg_to_send)

    data = sock.recv(1024)
    msg_recvd = message_parsing.parse_message(data)
    print "received {}".format(msg_recvd)
    client_id = int(msg_recvd.payload)
            
    data = sock.recv(1024)
    print "received {}".format(message_parsing.parse_message(data))

    data = sock.recv(1024)
    msg_recvd = message_parsing.parse_message(data)
    print "received {}".format(msg_recvd)
    player_num = int(msg_recvd.payload)

    p1_board = []
    p1_board.append([])
    p1_board.append([])
    p1_board.append([])
    p1_board[0].append("-")
    p1_board[0].append("-")
    p1_board[0].append("-")
    p1_board[1].append("-")
    p1_board[1].append("-")
    p1_board[1].append("-")
    p1_board[2].append("-")
    p1_board[2].append("-")
    p1_board[2].append("-")

    p2_board = []
    p2_board.append([])
    p2_board.append([])
    p2_board.append([])
    p2_board[0].append("-")
    p2_board[0].append("-")
    p2_board[0].append("-")
    p2_board[1].append("-")
    p2_board[1].append("-")
    p2_board[1].append("-")
    p2_board[2].append("-")
    p2_board[2].append("-")
    p2_board[2].append("-")

    def update_board(board, move, marker):
        if move == 1:
            board[0][0] = marker
        elif move == 2:
            board[0][1] = marker
        elif move == 3:
            board[0][2] = marker
        elif move == 4:
            board[1][0] = marker
        elif move == 5:
            board[1][1] = marker
        elif move == 6:
            board[1][2] = marker
        elif move == 7:
            board[2][0] = marker
        elif move == 8:
            board[2][1] = marker
        elif move == 9:
            board[2][2] = marker

    def print_board(board):
        print board[0][0], "|", board[0][1], "|", board[0][2]
        print "--+---+--"
        print board[1][0], "|", board[1][1], "|", board[1][2]
        print "--+---+--"
        print board[2][0], "|", board[2][1], "|", board[2][2]
    
    print "Starting Game 1 from Idle"

    if player_num == 0:
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p2_board, move, "X")
        print_board(p2_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="5")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p2_board, 5, "O")
        print_board(p2_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p2_board, move, "X")
        print_board(p2_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="2")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p2_board, 2, "O")
        print_board(p2_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p2_board, move, "X")
        print_board(p2_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="7")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p2_board, 7, "O")
        print_board(p2_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p2_board, move, "X")
        print_board(p2_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="6")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p2_board, 6, "O")
        print_board(p2_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p2_board, move, "X")
        print_board(p2_board)
        if test_reset:
            msg_to_send = message_creation.create_message(1, message.RESET, client_id=client_id, payload="Cat Game")
        else:
            msg_to_send = message_creation.create_message(1, message.GAMEEND, client_id=client_id, payload="Cat Game")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
    else:
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="1")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p1_board, 1, "X")
        print_board(p1_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p1_board, move, "O")
        print_board(p1_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="9")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p1_board, 9, "X")
        print_board(p1_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p1_board, move, "O")
        print_board(p1_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="8")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p1_board, 8, "X")
        print_board(p1_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p1_board, move, "O")
        print_board(p1_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="3")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p1_board, 3, "X")
        print_board(p1_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        move = int(message_parsing.parse_message(data).payload)
        update_board(p1_board, move, "O")
        print_board(p1_board)
        msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="4")
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)
        update_board(p1_board, 4, "X")
        print_board(p1_board)
        data = sock.recv(1024)
        print "received {}".format(message_parsing.parse_message(data))
        if test_reset:
            msg_to_send = message_creation.create_message(1, message.RESETACK, client_id=client_id)
        else:
            msg_to_send = message_creation.create_message(1, message.GAMEENDACK, client_id=client_id)
        print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
        sock.send(msg_to_send)

    if test_twice:
        p1_board = []
        p1_board.append([])
        p1_board.append([])
        p1_board.append([])
        p1_board[0].append("-")
        p1_board[0].append("-")
        p1_board[0].append("-")
        p1_board[1].append("-")
        p1_board[1].append("-")
        p1_board[1].append("-")
        p1_board[2].append("-")
        p1_board[2].append("-")
        p1_board[2].append("-")

        p2_board = []
        p2_board.append([])
        p2_board.append([])
        p2_board.append([])
        p2_board[0].append("-")
        p2_board[0].append("-")
        p2_board[0].append("-")
        p2_board[1].append("-")
        p2_board[1].append("-")
        p2_board[1].append("-")
        p2_board[2].append("-")
        p2_board[2].append("-")
        p2_board[2].append("-")

        if test_reset:
            data = sock.recv(1024)
            msg_recvd = message_parsing.parse_message(data)
            print "received {}".format(msg_recvd)
            player_num = int(msg_recvd.payload)
    
            print "Starting Game 2 from Game Start"
        else:
            msg_to_send = message_creation.create_message(1, message.NEWGAMETYPE, payload="1")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)

            data = sock.recv(1024)
            msg_recvd = message_parsing.parse_message(data)
            print "received {}".format(msg_recvd)
            client_id = int(msg_recvd.payload)
            
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))

            data = sock.recv(1024)
            msg_recvd = message_parsing.parse_message(data)
            print "received {}".format(msg_recvd)
            player_num = int(msg_recvd.payload)

            print "Starting Game 2 from Idle"

        if player_num == 0:
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p2_board, move, "X")
            print_board(p2_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="5")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p2_board, 5, "O")
            print_board(p2_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p2_board, move, "X")
            print_board(p2_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="3")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p2_board, 3, "O")
            print_board(p2_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p2_board, move, "X")
            print_board(p2_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="8")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p2_board, 8, "O")
            print_board(p2_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p2_board, move, "X")
            print_board(p2_board)
            msg_to_send = message_creation.create_message(1, message.GAMEEND, client_id=client_id, payload="Player 1 Winner")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
        else:
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="1")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p1_board, 1, "X")
            print_board(p1_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p1_board, move, "O")
            print_board(p1_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="9")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p1_board, 9, "X")
            print_board(p1_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p1_board, move, "O")
            print_board(p1_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="7")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p1_board, 7, "X")
            print_board(p1_board)
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            move = int(message_parsing.parse_message(data).payload)
            update_board(p1_board, move, "O")
            print_board(p1_board)
            msg_to_send = message_creation.create_message(1, message.MOVE, client_id=client_id, payload="4")
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)
            update_board(p1_board, 4, "X")
            data = sock.recv(1024)
            print "received {}".format(message_parsing.parse_message(data))
            msg_to_send = message_creation.create_message(1, message.GAMEENDACK, client_id=client_id)
            print "sent ({} bytes): {}".format(len(msg_to_send), message_parsing.parse_message(msg_to_send))
            sock.send(msg_to_send)

    print "Done"
except Exception as e_inst:
    print "Exception: ", e_inst
finally:
    sock.close()