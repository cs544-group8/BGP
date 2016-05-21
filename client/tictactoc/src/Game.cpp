//
//  Game.cpp
//  tictactoc
//
//  Created by TJ Rhodes on 5/17/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#include "Game.hpp"

Game::Game(int id, int height, int width)
{
    m_id = id;
    m_height = height;
    m_width = width;
    m_game_board.resize(m_height);
    m_token.push_back("x");
    m_token.push_back("o");
    for(int row = 0; row < m_height; row++)
        m_game_board[row].resize(m_width);
}

Game::~Game()
{
    
}

void Game::showBoard()
{
    for(int row = 0; row < m_height; row++) {
        cout << endl << " " << m_game_board[row][0] << " ";
        for(int col = 1; col < m_width; col++) {
            cout << "| " << m_game_board[row][col] << " ";
        }
        if (row < m_height - 1) {
            cout << endl << "---";
            for(int col = 1; col < m_width; col++) {
                cout << "+---";
            }
        }
    }
    cout << endl;
}

void Game::resetGameboard()
{
    int position = 1;
    for(int row = 0; row < m_height; row++) {
        for(int col = 0; col < m_width; col++) {
            m_game_board[row][col] = to_string(position);
            ++position;
        }
    }
}

bool Game::validMove(string pos, int player)
{
    int position = stoi(pos);
    int row,col;
    if(position < 1 || position > m_width*m_height) // check for valid position on board
        return false;
    
    row = (position-1)/m_height;
    col = (position-1)%m_width;
    
    if(m_game_board[row][col].compare(pos) == 0) {   // check if position available
        m_game_board[row][col] = m_token[player];
        return true;
    }
    
    else
        return false;
}

bool Game::isGameOver()
{
    int position = 1;    
    for(int row = 0; row < m_height; row++) {
        for(int col = 0; col < m_width; col++) {
            if(m_game_board[row][col].compare(to_string(position)) == 0) {   // check if positions available
                return false;   // game is not over
            }
            ++position;
        }
    }
    return true; // no available moves found
}