//
//  Client.cpp
//  tictactoc
//
//  Created by TJ Rhodes on 5/17/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#include "Client.hpp"

using namespace ClientEnums;

Client::Client(Game game)
{
    m_game = game;
}

Client::~Client()
{
    
}

void Client::start(int initial_state)
{
    m_client_state = initial_state;
}

void Client::run()
{
    bool done = false;
    
    while(!done) {
        switch(m_client_state) {
            case IDLE:
                m_client_state = requestGame();
                break;
                
            case ASSIGN_ID:
                m_client_state = assignID();
                break;
                
            case FIND_OPP:
                m_client_state = findOpponent();
                break;
                
            case RECV_MOVE:
                m_client_state = incomingMove();
                drawLine();
                break;
                
            case SEND_MOVE:
                m_client_state = outgoingMove();
                drawLine();
                break;
                
            case GAME_END:
                m_client_state = gameOver();
                drawLine();
                break;
                
            default:
                done = true;
                break;
        }
    }
}

int Client::requestGame()
{
    bool success = true; // delete later
    
    cout << "Connect to server by entering ip address or hostname:" << endl;
    cout << "e.g. 192.168.23.136 or GameServer" << endl;
    getline(cin, m_server_address);
    
    cout << "Enter game would you like to play:" << endl;
    cout << "(See BGP manual for valid game types)" << endl;
    getline(cin, m_game_ID);
    
    send("Sent game id to server address"); // server needs to validate this ID
    
    if(success)
        return ASSIGN_ID;
    else {
        m_reason = "Failed to connect to: " + m_server_address;
        return GAME_END;
    }
}

int Client::assignID()
{
    bool success = true; // delete later
    
    m_client_id = receive("Received client id", 123456);
    
    if(success)
        return FIND_OPP;
    else {
        m_reason = "No client ID received from server";
        return GAME_END;
    }
}

int Client::findOpponent()
{
    bool wait = true;   // delete later
    bool success = true; // delete later
    
    send("Sent find opponent message to server");
    
    if(wait)
        cout << "Server is looking for opponent..." << endl;
    
    if(success) {
        m_player = receive("Server found opponent", GameEnums::PLAYER1);    // server assigns client as player 1 or 2
        
        m_game.showBoard();
        if(m_player == GameEnums::PLAYER1)
            return SEND_MOVE;
        else if(m_player == GameEnums::PLAYER2)
            return RECV_MOVE;
        else {
            m_reason = "Invalid player ID assigned";
            return GAME_END;
        }
    }
    else {
        m_reason = "Server failed to find opponent. Try again later.";
        return GAME_END;
    }
}

int Client::incomingMove()
{
    bool success = true; // delete later
    
    if(!m_game.isGameOver()) {
        cout << "Waiting for move from opponent" << endl;
        getline(cin, m_move);
        
        if(success) {
            m_game.validMove(m_move, GameEnums::PLAYER2);
            return SEND_MOVE;
        }
        
        else {
            m_reason = "No move received from opponent";
            return GAME_END;
        }
    }
    else {
        m_reason = "Game over";
        return GAME_END;
    }
}

int Client::outgoingMove()
{
    if(!m_game.isGameOver()) {
        cout << "Enter your move:" << endl;
        cout << "e.g. 2 or 7" << endl;
        getline(cin, m_move);
        
        if(m_game.validMove(m_move, m_player)) {
            send("Sent move: " + m_move);
            return RECV_MOVE;
        }
        else {
            cout << "Invalid move. Try again" << endl;
            return SEND_MOVE;
        }
    }
    
    else {
        m_reason = "Game over";
        return GAME_END;
    }
}

int Client::gameOver()
{
    send("Sent reason for game over");
    cout << "Quitting application..." << endl;
    return -1;
}

void Client::drawLine()
{
    cout << "----------------------------------------------------" << endl;
}

void Client::send(string message)
{
    cout << "***" << message << "***"<< endl;
}

int Client::receive(string message, int data)
{
    cout << "***" << message << "***" << endl;
    return data;
}