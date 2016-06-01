//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: client.hpp
//  Description: header file for client object

#ifndef client_hpp
#define client_hpp

#include <stdio.h>
#include <iostream>
#include <cstring>
#include "game.hpp"
#include "pdu.hpp"
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>


using namespace std;

class Client
{
public:
    Client(Game game);
    ~Client();

    // Communication
    string m_server_address;
    int m_port;
    int m_sock;
    struct sockaddr_in server;
    bool connected(string addr, int port);
    void disconnect();
    string lookupHostname(string hostname);
    bool sent(int message, string data);
    bool receivedHeader(const PDU & pdu);
    bool receivedPayload(const PDU & pdu);

    // Game
    Game m_game;
    string m_game_ID;
    string m_move;
    string m_last_move;
    int m_opp_move;
    int m_player;
    int m_reason;
    bool m_resend_move;
    bool m_gameover;

    // States
    int m_client_state;
    void start(int initial_state);              // Set initial client state
    void run();                                 // Run the client state machine
    int requestGame();
    int assignID();
    int findOpponent();
    int assignPlayer();
    int incomingMove();
    int outgoingMove();
    int requestReset();
    int resetResponse();
    int gameOver();
    void drawLine();

    // Misc
    unsigned char m_version;
    unsigned int m_client_id;
    int startPosition(int player);
    int opponent(int player);
    string reason(int r);
};

namespace ClientEnums
{
    enum States {   IDLE,
                    ASSIGN_ID,
                    FIND_OPP,
                    GAME_START,
                    RECV_MOVE,
                    SEND_MOVE,
                    RECV_RESET,
                    SEND_RESET,
                    GAME_END
                    };
}

#endif /* client_hpp */
