//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: game.cpp
//  Description: Source file for game object. Logic for game is handled here

#include "game.hpp"

using namespace GameEnums;

Game::Game()
{
    m_token.resize(2);
}

Game::Game(int id, int height, int width)
{
    m_id = id;
    m_height = height;
    m_width = width;
    m_game_board.resize(m_height);
    m_token.resize(2);
    for(int row = 0; row < m_height; row++)
        m_game_board[row].resize(m_width);
    resetBoard();
    m_token[PLAYER1] = "x";
    m_token[PLAYER2] = "o";
}

void Game::operator=(const Game &G)
{
    m_id = G.m_id;
    m_height = G.m_height;
    m_width = G.m_width;
    m_game_board.resize(m_height);
    m_token[PLAYER1] = G.m_token[0];
    m_token[PLAYER2] = G.m_token[1];
    m_game_board = G.m_game_board;
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

void Game::resetBoard()
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
    int position;

    try {
        position = stoi(pos);
    }

    catch(std::exception& e) {
        return false;
    }

    int row,col;
    if(position < 1 || position > m_width*m_height) // check for valid position on board
        return false;

    row = (position-1)/m_height;
    col = (position-1)%m_width;

    if(m_game_board[row][col].compare(pos) == 0) {   // check if position available
        m_game_board[row][col] = m_token[player];
        showBoard();
        return true;
    }

    else
        return false;
}

bool Game::isGameOver()
{
    for(int row = 0; row < m_height; row++) {
        if(m_game_board[row][0] == m_game_board[row][1] && m_game_board[row][0] == m_game_board[row][2])
            return true; // horizontal victory
    }

    for(int col = 0; col < m_width; col++) {
        if(m_game_board[0][col] == m_game_board[1][col] && m_game_board[0][col] == m_game_board[2][col])
            return true; // vertical victory
    }

    if(m_game_board[0][0] == m_game_board[1][1] && m_game_board[0][0] == m_game_board[2][2])
        return true; // diagonal victory

    if(m_game_board[0][2] == m_game_board[1][1] && m_game_board[0][2] == m_game_board[2][0])
        return true; // diagonal victory

    int position = 1;
    for(int row = 0; row < m_height; row++) {
        for(int col = 0; col < m_width; col++) {
            if(m_game_board[row][col].compare(to_string(position)) == 0) {
                return false;   // still available moves
            }
            ++position;
        }
    }

    return true;    // no available moves found
}
