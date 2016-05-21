//
//  Game.hpp
//  tictactoc
//
//  Created by TJ Rhodes on 5/17/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#ifndef Game_hpp
#define Game_hpp

#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Game
{
public:
    Game(int id, int height, int width);
    ~Game();
    
    int m_id;
    int m_width;
    int m_height;
    int m_player;
    vector<string> m_token;   // player token
    vector< vector<string> > m_game_board;
    
    void showBoard();
    void resetGameboard();
    bool validMove(string position, int player);
    bool isGameOver();
};

namespace GameEnums
{
    enum Player {PLAYER1, PLAYER2};
}

#endif /* Game_hpp */
