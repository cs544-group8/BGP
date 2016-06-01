//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: game.hpp
//  Description: header file for game object

#ifndef game_hpp
#define game_hpp

#include <stdio.h>
#include <iostream>
#include <cstring>
#include <vector>

using namespace std;

class Game
{
public:
    Game();
    Game(int id, int height, int width);
    ~Game();

    int m_id;
    int m_width;
    int m_height;
    vector<string> m_token;   // player token
    vector< vector<string> > m_game_board;

    void showBoard();
    void resetBoard();
    bool validMove(string position, int player);
    bool isGameOver();
    void operator=(const Game &G);
};

namespace GameEnums
{
    enum Player {PLAYER1, PLAYER2};

    enum GameEndReasons {
            GAMEOVER,
            OPPLEFT,
            QUIT
    };
}

#endif /* game_hpp */
