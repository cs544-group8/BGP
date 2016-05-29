//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: game.cpp
//  Description: Source file for client object. Logic for BGP protocol state is handled here

#include "client.hpp"

using namespace ClientEnums;
using namespace PDUEnums;

Client::Client(Game game)
{
    m_game = game;
    m_client_id = 0x0000;
    m_port = 9999;
    m_sock = -1;
    m_version = 1;
}

Client::~Client()
{
    
}

void Client::start(int initial_state)
{
    m_client_state = initial_state;
}

void Client::run()
{
    bool done = false;
    
    while(!done) {
        switch(m_client_state) {
            case IDLE:
                m_client_state = requestGame();
                break;
                
            case ASSIGN_ID:
                m_client_state = assignID();
                break;
                
            case FIND_OPP:
                m_client_state = findOpponent();
                break;
                
            case RECV_MOVE:
                m_client_state = incomingMove();
                drawLine();
                break;
                
            case SEND_MOVE:
                m_client_state = outgoingMove();
                drawLine();
                break;
                
            case GAME_END:
                m_client_state = gameOver();
                drawLine();
                break;
                
            default:
                done = true;
                break;
        }
    }
}

int Client::requestGame()
{
    cout << "Connect to server by entering ip address or hostname:" << endl;
    cout << "e.g. 192.168.23.136 or GameServer" << endl;
    getline(cin, m_server_address);
    
    if (connected(m_server_address, m_port)) {    // Successful connection
        cout << "Enter game you would like to play:" << endl;
        cout << "(See BGP manual for valid game types)" << endl;
        getline(cin, m_game_ID);
        
        if(!sent(NEWGAMETYPE, m_game_ID)) {       // Send failed
            cerr << "Send error in IDLE" << endl;
            return -1;
        }
        
        else {
            cout << "Sent game id to server" << endl;
            return -1;
        }
    }
    
    return -1;
}

int Client::assignID()
{
    PDU in_pdu;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case INVGAMETYPE:
                cout << "Invalid game id" << endl;
                return IDLE;
            case CLIENTIDASSIGN:
                if(receivedPayload(in_pdu)) { // payload received
                    try {
                        m_client_id = in_pdu.m_header.m_client_ID;
                    }
                    catch (std::invalid_argument&){
                        cerr << "Invaid client id type. Must be unsigned int: " <<  in_pdu.m_header.m_client_ID << endl;
                        return ASSIGN_ID;
                    }
                    return FIND_OPP;
                }
                else {
                    cerr << "No payload received from server in ASSIGN_ID" << endl;
                    return ASSIGN_ID;
                }

            default:
                cerr << "Invalid message type in ASSIGN_ID: " << in_pdu.m_header.m_message_type << endl;
                return ASSIGN_ID;
        }
    }
    
    else {
        cout << "No message received from server in ASSIGN_ID" << endl; // time out case
        return IDLE;
    }
}

int Client::findOpponent()
{
//    bool wait = true;   // delete later
//    bool success = true; // delete later
//    
//    send("Sent find opponent message to server");
//    
//    if(wait)
//        cout << "Server is looking for opponent..." << endl;
//    
//    if(success) {
//        m_player = receive("Server found opponent", GameEnums::PLAYER1);    // server assigns client as player 1 or 2
//        
//        m_game.showBoard();
//        if(m_player == GameEnums::PLAYER1)
//            return SEND_MOVE;
//        else if(m_player == GameEnums::PLAYER2)
//            return RECV_MOVE;
//        else {
//            m_reason = "Invalid player ID assigned";
//            return GAME_END;
//        }
//    }
//    else {
//        m_reason = "Server failed to find opponent. Try again later.";
//        return GAME_END;
//    }
    return -1;
}

int Client::incomingMove()
{
//    bool success = true; // delete later
//    
//    if(!m_game.isGameOver()) {
//        cout << "Waiting for move from opponent" << endl;
//        getline(cin, m_move);
//        
//        if(success) {
//            m_game.validMove(m_move, GameEnums::PLAYER2);
//            return SEND_MOVE;
//        }
//        
//        else {
//            m_reason = "No move received from opponent";
//            return GAME_END;
//        }
//    }
//    else {
//        m_reason = "Game over";
//        return GAME_END;
//    }
    return -1;
}

int Client::outgoingMove()
{
//    if(!m_game.isGameOver()) {
//        cout << "Enter your move:" << endl;
//        cout << "e.g. 2 or 7" << endl;
//        getline(cin, m_move);
//        
//        if(m_game.validMove(m_move, m_player)) {
//            send("Sent move: " + m_move);
//            return RECV_MOVE;
//        }
//        else {
//            cout << "Invalid move. Try again" << endl;
//            return SEND_MOVE;
//        }
//    }
//    
//    else {
//        m_reason = "Game over";
//        return GAME_END;
//    }
    return -1;
}

int Client::gameOver()
{
//    send("Sent reason for game over");
//    cout << "Quitting application..." << endl;
    return -1;
}

void Client::drawLine()
{
    cout << "----------------------------------------------------" << endl;
}

bool Client::connected(string address , int port)
{
    //create socket if it is not already created
    if(m_sock == -1)
    {
        //Create socket
        m_sock = socket(AF_INET , SOCK_STREAM , 0);
        if (m_sock == -1)
        {
            cerr << ("Could not create socket") << endl;
        }
        
        cout << "Socket created" << endl;
    }
    else    {   /* OK , nothing */  }
    
    server.sin_addr.s_addr = inet_addr( address.c_str() );
    server.sin_family = AF_INET;
    server.sin_port = htons( m_port );
    
    //Connect to remote server
    if (connect(m_sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        cerr << "Failed to connect to " << m_server_address << endl;
        return false;
    }
    
    cout<<"Connected to " << m_server_address << " on port " << m_port << endl;
    return true;
}

bool Client::sent(int message, string data)
{
    PDU out_pdu;
    unsigned char prep_data[data.length()];
    strcpy((char *) prep_data, data.c_str());
    
    out_pdu.buildPDU(m_client_id, message, prep_data);
    
    if (out_pdu.m_header.m_length > 0) {    // include payload
//        unsigned char out[out_pdu.m_header.m_length + 8];   // payload size + fixed header
//        memcpy(out, &out_pdu.m_header, sizeof(8));
//        memcpy(out+8, &out_pdu.m_payload, sizeof(out_pdu.m_header.m_length));

        unsigned char out[9] = {1,0,1,0,0,0,0,0,1};
        
        if(send(m_sock, (char *) out, sizeof(out),0) < 0) {              // Send payload
            cerr << "Failed to send client id" << endl;
            return false;
        }
    }
    
    else { // header only
        unsigned char out[8];   // payload size + fixed header
        memcpy(out, &out_pdu.m_header, sizeof(8));
        
        if(send(m_sock, (char *) out, 8,0) < 0) {              // Send payload
            cerr << "Failed to send client id" << endl;
            return false;
        }
    }
    
    return true; // successfully sent message
}

bool Client::receivedHeader(const PDU &in_pdu)
{
    char buffer[8]; // fixed header size
    
    if(recv(m_sock, buffer, sizeof(buffer), 0) < 0) {
        cerr << "Receive header failed" << endl;
        return false;
    }
    
//    memcpy(&in_pdu.m_header, buffer, sizeof(buffer));   // no idea if this works
    
    if(in_pdu.m_header.m_version != m_version) {  // invalid version
        cerr << "Invalid header version" << endl;
        return false;
    }
    
    if(in_pdu.m_header.m_client_ID != m_client_id) {  // invalid client ID
        cerr << "Invalid header client id" << endl;
        return false;
    }
    
    return true;
}

bool Client::receivedPayload(const PDU &in_pdu)
{
    char buffer[in_pdu.m_header.m_length]; // payload size
    
    if(recv(m_sock, buffer, sizeof(buffer), 0) < 0) {
        cerr << "Receive payload failed" << endl;
        return false;
    }
    
//    memcpy(&in_pdu.m_payload.m_data, buffer, sizeof(buffer));   // no idea if this works
    
    return true;
}