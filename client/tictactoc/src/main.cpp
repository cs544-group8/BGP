//
//  main.cpp
//  tictactoc
//
//  Created by TJ Rhodes on 5/16/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#include "Client.hpp"
#include "Game.hpp"

using namespace std;
using namespace ClientEnums;

int main(int argc, const char * argv[]) {
    Game tictactoe(1,3,3);  // game_ID, height, width
        
    Client client(tictactoe); // set client game

    client.start(IDLE);
    client.run();
    
    return 0;
}
