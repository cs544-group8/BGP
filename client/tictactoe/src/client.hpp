#ifndef client_hpp
#define client_hpp

#include <stdio.h>
#include <iostream>
#include <string>
#include "game.hpp"

using namespace std;

class Client
{
public:
    Client(Game game);
    ~Client();
    
//    Pdu pdu;
    Game m_game;
    string m_server_address;
    string m_game_ID;
    string m_reason;
    string m_move;
    
    int m_client_state;
    int m_player;
    long m_client_id;
    
    void start(int initial_state);              // Set initial client state
    void run();                                 // Run the client state machine
    int requestGame();
    int assignID();
    int findOpponent();
    int incomingMove();
    int outgoingMove();
    int gameOver();
    void send(string message);
    int receive(string message, int data);
    void drawLine();    
};

namespace ClientEnums
{
    enum States {   IDLE,
                    ASSIGN_ID,
                    FIND_OPP,
                    RECV_MOVE,
                    SEND_MOVE,
                    GAME_END
                    };
    enum Messages { NEWGAMETYPE,
                    CLIENTIDASSIGN,
                    FINDOPP,
                    FOUNDOPP,
                    REQMOVE,
                    OPPMOVE,
                    MOVE,
                    GAMEEND,
                    GAMEENDACK
                    };
    enum Errors {   INVGAMETYPE
                    };
}

#endif /* client_hpp */