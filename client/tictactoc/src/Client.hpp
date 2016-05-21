//
//  Client.hpp
//  tictactoc
//
//  Created by TJ Rhodes on 5/17/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#ifndef Client_hpp
#define Client_hpp

#include <stdio.h>
#include <iostream>
#include <string>
#include "Game.hpp"

using namespace std;

class Client
{
public:
    Client(Game game);
    ~Client();
    
//    Pdu pdu;
    Game game;
    string server_address;
    int client_state;
    
    
    void start(int initial_state);              // Set initial client state
    void run();                                 // Run the client state machine
    
};

namespace ClientEnums
{
    enum States {   IDLE,
                    ESTABLISH_GAME,
                    ASSIGN_ID,
                    FIND_OPP,
                    REQ_MOVE,
                    SEND_MOVE,
                    WAIT_MOVE,
                    GAME_END
                    };
    enum Messages { NEWGAMETYPE,
                    CLIENTIDASSIGN,
                    FINDOPP,
                    WAITFOROPP,
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

#endif /* Client_hpp */
