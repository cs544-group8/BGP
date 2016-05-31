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
    m_client_id = 0;
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
                
            case GAME_START:
                m_client_state = assignPlayer();
                m_game.resetGameboard();
                break;
                
            case RECV_MOVE:
                m_client_state = incomingMove();
                drawLine();
                break;
                
            case SEND_MOVE:
                m_client_state = outgoingMove();
                drawLine();
                break;
                
            case SEND_RESET:
                m_client_state = requestReset();
                break;
                
            case RECV_RESET:
                m_client_state = resetResponse();
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
            cerr << "BGP: Send error in IDLE" << endl;
            return IDLE;
        }
        
        else {
            cout << "Sent game id to server" << endl;
            return ASSIGN_ID;
        }
    }
    
    return -1;  // quit application if connection fails
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
                        m_client_id = atoi((char*)in_pdu.m_payload.m_data);
                    }
                    catch (std::invalid_argument&){
                        cerr << "BGP: Invaid client id type. Must be unsigned int" << endl;
                        return ASSIGN_ID;
                    }
                    return FIND_OPP;
                }
                else {
                    cerr << "BGP: No payload received from server in ASSIGN_ID" << endl;
                    return ASSIGN_ID;
                }

            default:
                cerr << "BGP: Invalid message type in ASSIGN_ID: " << in_pdu.m_header.m_message_type << endl;
                return ASSIGN_ID;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in ASSIGN_ID" << endl; // time out case
        disconnect();
        return IDLE;
    }
}

int Client::findOpponent()
{
    PDU in_pdu;
    
    cout << "Server is looking for opponent..." << endl;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case FOUNDOPP:
                if(receivedPayload(in_pdu)) { // payload received
                    // ignore payload
                    return GAME_START;
                }
                else {
                    cerr << "BGP: No payload received from server in FIND_OPP" << endl;
                    return FIND_OPP;
                }
            default:
                cerr << "BGP: Invalid message type in FIND_OPP: " << in_pdu.m_header.m_message_type << endl;
                return FIND_OPP;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in FIND_OPP" << endl; // time out case
        disconnect();
        return IDLE;
    }
}

int Client::assignPlayer()
{
    PDU in_pdu;
    m_gameover = false;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case PLAYERASSIGN:
                if(receivedPayload(in_pdu)) { // payload received
                    try {
                        m_player = atoi((char*)in_pdu.m_payload.m_data);
                    }
                    catch (std::invalid_argument&){
                        cerr << "BGP: Invaid player number. Must be a number" << endl;
                        return GAME_START;
                    }
                    
                    return startPosition(m_player);
                }
                else {
                    cerr << "BGP: No payload received from server in GAME_START" << endl;
                    return GAME_START;
                }
            default:
                cerr << "BGP: Invalid message type in GAME_START: " << in_pdu.m_header.m_message_type << endl;
                return GAME_START;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in GAME_START" << endl; // time out case
        disconnect();
        return IDLE;
    }
}

int Client::incomingMove()
{
    PDU in_pdu;
    
    cout << "Waiting for opponent..." << endl;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case MOVE:
                if(receivedPayload(in_pdu)) { // payload received
                    try {
                        m_opp_move = atoi((char*)in_pdu.m_payload.m_data);
                    }
                    catch (std::invalid_argument&){
                        cerr << "BGP: Invaid player number. Must be a number" << endl;
                        return RECV_MOVE;
                    }
                    
                    if(m_game.validMove(to_string(m_opp_move), GameEnums::PLAYER2))
                        return SEND_MOVE;
                    
                    else {
                        if(!sent(INVMOVE, "")) {       // Send failed
                            cerr << "BGP: Send error in RECV_MOVE, INVMOVE message" << endl;
                            return IDLE;
                        }
                        return RECV_MOVE;
                    }
                }
                else {
                    cerr << "BGP: No payload received from server in RECV_MOVE, MOVE message" << endl;
                    return RECV_MOVE;
                }
            case INVMOVE:
                m_resend_move = true;
                return SEND_MOVE;
                
            case RESET:
                return RECV_RESET;
                
            case GAMEEND:
                if(receivedPayload(in_pdu)) { // payload received
                    try {
                        m_reason = atoi((char*)in_pdu.m_payload.m_data);
                    }
                    catch (std::invalid_argument&){
                        cerr << "BGP: Invaid reason. Must be a number" << endl;
                        return RECV_MOVE;
                    }
                    m_gameover = true;
                    return GAME_END;
                }
                else {
                    cerr << "BGP: No payload received from server in RECV_MOVE, GAMEEND message" << endl;
                    return RECV_MOVE;
                }
                
            default:
                cerr << "BGP: Invalid message type in RECV_MOVE: " << in_pdu.m_header.m_message_type << endl;
                return RECV_MOVE;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in RECV_MOVE" << endl; // time out case
        disconnect();
        return IDLE;
    }
}

int Client::outgoingMove()
{
    if(!m_game.isGameOver()) {
        if(m_resend_move) {
            if(!sent(MOVE, m_last_move)) {       // Send failed
                cerr << "BGP: Send error in SEND_MOVE, last MOVE message" << endl;
                disconnect();
                return IDLE;
            }
            m_resend_move = false;
            return RECV_MOVE;
        }
        
        cout << "Enter your move:" << endl;
        cout << "e.g. 2 or 7" << endl;
        getline(cin, m_move);
            
        switch(m_move[0]) {
            case 'Q':
            case 'q':
                m_reason = GameEnums::QUIT;
                if(!sent(GAMEEND, to_string(m_reason))) {       // Send failed
                    cerr << "BGP: Send error in SEND_MOVE, GAMEEND message" << endl;
                    disconnect();
                    return IDLE;
                }
                return GAME_END;
                
            case 'R':
            case 'r':
                if(!sent(RESET, "")) {       // Send failed
                    cerr << "BGP: Send error in SEND_MOVE, RESET message" << endl;
                    disconnect();
                    return IDLE;
                }
                return SEND_RESET;
                
            default:
                if(m_game.validMove(m_move, m_player)) {
                    m_last_move = m_move;
                    if(!sent(MOVE, m_move)) {       // Send failed
                        cerr << "BGP: Send error in SEND_MOVE, MOVE message" << endl;
                        disconnect();
                        return IDLE;
                    }
                    return RECV_MOVE;
                }
                else {
                    cout << "Invalid move. Try again." << endl;
                    return SEND_MOVE;
                }
                return RECV_MOVE;
        }
    }
    
    else {
        m_reason = GameEnums::GAMEOVER;
        if(!sent(GAMEEND, to_string(m_reason))) {       // Send failed
            cerr << "BGP: Send error in SEND_MOVE, INVMOVE message" << endl;
            disconnect();
            return IDLE;
        }
        return GAME_END;
    }
}

int Client::requestReset()
{
    PDU in_pdu;
    
    cout << "Waiting for reset response from opponent..." << endl;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case RESETACK:
                return GAME_START;
                
            case RESETNACK:
                return SEND_MOVE;
            
            default:
                cerr << "BGP: Invalid message type in SEND_RESET: " << in_pdu.m_header.m_message_type << endl;
                return SEND_RESET;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in SEND_RESET" << endl; // time out case
        disconnect();
        return IDLE;
    }
}

int Client::resetResponse()
{
    string response;
    
    cout << "Opponent requested restart" << endl;
    cout << "Accept or Decline [y/n]" << endl;
    getline(cin, response);
    
    switch(response[0]) {
        case 'Y':
        case 'y':
            if(!sent(RESETACK, "")) {       // Send failed
                cerr << "BGP: Send error in RECV_RESET, RESETACK message" << endl;
                disconnect();
                return IDLE;
            }
            return GAME_START;
        case 'N':
        case 'n':
            if(!sent(RESETNACK, "")) {       // Send failed
                cerr << "BGP: Send error in RECV_RESET, RESETNACK message" << endl;
                disconnect();
                return IDLE;
            }
            return RECV_MOVE;
        default:
            cout << "Invalid response. Try again." << endl;
            return RECV_RESET;
    }
}

int Client::gameOver()
{
    PDU in_pdu;
    
    cout << "Gameover: ";
    
    if(!m_gameover) {
        if(receivedHeader(in_pdu)) { // valid header received
            switch(in_pdu.m_header.m_message_type) {
                case GAMEENDACK:
                    cout << reason(m_reason) << endl;
                default:
                    cerr << "BGP: Invalid message type in GAME_END: " << in_pdu.m_header.m_message_type << endl;
                    return GAME_END;
            }
        }
        else {
            cerr << "BGP: No message received from server in GAME_END" << endl; // time out case
            disconnect();
            return IDLE;
        }
    }
    
    else {
        if(!sent(GAMEENDACK, "")) {       // Send failed
            cerr << "BGP: Send error in GAME_END, GAMEENDACK message" << endl;
            disconnect();
            return IDLE;
        }
        cout << reason(m_reason) << endl;
        return IDLE;
    }
}

void Client::drawLine()
{
    cout << "----------------------------------------------------" << endl;
}

int Client::startPosition(int player)
{    
    switch (player) {
        case GameEnums::PLAYER1:
            cout << "You are player " << m_player << endl;
            return SEND_MOVE;
        case GameEnums::PLAYER2:
            cout << "You are player " << m_player << endl;
            return RECV_MOVE;
        default:
            cout << "BGP: Cannot assign player number: " << player << endl;
            return GAME_START;
    }
}

string Client::reason(int r)
{
    switch(r) {
        case GameEnums::GAMEOVER:
            return "Gameplay has finished";
        case GameEnums::OPPLEFT:
            return "Oppenent ended the game";
        case GameEnums::QUIT:
            return "You ended the game";
        default:
            cout << "BGP: Invalid game end reason: " << r << endl;
            return "";
    }
}

void Client::disconnect()
{
    cout << "Disconnecting from " << m_server_address << " on port " << m_port << "..." << endl;
    shutdown(m_sock, SHUT_RDWR);
    close(m_sock);
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
    
    if(address.find(".") == string::npos) { // hostname
        address = string(lookupHostname(address));
    }
    
    server.sin_addr.s_addr = inet_addr( address.c_str() );
    server.sin_family = AF_INET;
    server.sin_port = htons( m_port );
    
    //Connect to remote server
    if (connect(m_sock , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        cerr << "Failed to connect to " << m_server_address << endl;
        return false;
    }
    
    else {
        cout<<"Connected to " << m_server_address << " on port " << m_port << endl;
        return true;
    }
}

string Client::lookupHostname(string hostname)
{
    struct hostent *he;
    struct in_addr **addr_list;
    
    if ( (he = gethostbyname( hostname.c_str() ) ) == NULL)
    {
        // get the host info
        perror("gethostbyname");
        return hostname;
    }
    
    addr_list = (struct in_addr **) he->h_addr_list;
    
    return string(inet_ntoa(*addr_list[0]));
}

bool Client::sent(int message, string data)
{
    PDU out_pdu;
    out_pdu.buildPDU(m_client_id, message, data);
    
    if (out_pdu.m_header.m_length > 0) {    // include payload
        const int size = out_pdu.m_header.m_length + 8;
        unsigned char out[size];            // fixed header + payload size
        memcpy(out, &out_pdu.m_header, 8);
        memcpy(out+8, &out_pdu.m_payload, out_pdu.m_header.m_length);
        
        if(send(m_sock, out, size,0) < 0) {              // Send pdu
            cerr << "Failed to send client id" << endl;
            return false;
        }
    }
    
    else { // header only
        unsigned char out[8];   // payload size + fixed header
        memcpy(out, &out_pdu.m_header, 8);
        
        if(send(m_sock, out, 8,0) < 0) {              // Send pdu
            cerr << "Failed to send client id" << endl;
            return false;
        }
    }
    
    return true; // successfully sent message
}

bool Client::receivedHeader(const PDU &in_pdu)
{
    unsigned char buffer[8]; // fixed header size
    
    if(recv(m_sock, buffer, 8, 0) < 0) {
        cerr << "Receive header failed" << endl;
        return false;
    }
    
    memcpy((char *)&in_pdu.m_header, buffer, 8);   // no idea if this works
    
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
    unsigned char buffer[in_pdu.m_header.m_length]; // payload size
    
    if(recv(m_sock, buffer, in_pdu.m_header.m_length, 0) < 0) {
        cerr << "Receive payload failed" << endl;
        return false;
    }
    
    memcpy((char *)&in_pdu.m_payload.m_data, buffer, in_pdu.m_header.m_length);   // no idea if this works
    
    return true;
}