#ifndef game_hpp
#define game_hpp

#include <stdio.h>
#include <iostream>
#include <string>
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
    void resetGameboard();
    bool validMove(string position, int player);
    bool isGameOver();
    void operator=(const Game &G);
};

namespace GameEnums
{
    enum Player {PLAYER1, PLAYER2};
}

#endif /* game_hpp */