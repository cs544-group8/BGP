//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: main.cpp
//  Description: 'main' for tictactoe application

#include "client.hpp"
#include "game.hpp"

using namespace std;
using namespace ClientEnums;

// Main method to start the client
int main(int argc, const char * argv[]) {
    Game tictactoe(1,3,3);    // game_ID, height, width
        
    Client client(tictactoe); // set client game
    
    client.start(IDLE);
    client.run();
    
    return 0;
}