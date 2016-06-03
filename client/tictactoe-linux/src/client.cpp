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

// Client class constructor to initialize static variables
Client::Client(Game game)
{
    m_game = game;
    m_client_id = 0;
    m_port = 9999;
    m_sock = -1;
    m_version = 1;
    m_gameover = false;
}

// Default class constructor
Client::~Client()
{
    
}

// method to initialize the client state
void Client::start(int initial_state)
{
    m_client_state = initial_state;
}

// method to start the game by obtaining the server address from the player
// implements the client finite state machine
void Client::run()
{
    bool done = false;
    
    cout << "Connect to server by entering ip address or hostname:" << endl;
    cout << "e.g. 192.168.23.136 or GameServer" << endl;
    getline(cin, m_server_address);
    
    // Service: The client shall connect to the server on a hardcoded port number,
    // which defaults to port number (port 9999).

    if (connected(m_server_address, m_port)) {    // Successful connection
        m_client_state = requestGame();
    }
    else {
        m_client_state = -1;
    }
    
    // Stateful: Both client and server must implement, check and validate the statefulness of the BGP protocol DFA.

    while(!done) {
        switch(m_client_state) {
            case IDLE:
                m_client_id = 0;
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
                m_game.resetBoard();
                m_game.showBoard();
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

// method to ask the player which game they want to play
// implemented for tic-tac-toe board game
// method sends a New Game Type message to the server
// sets the next client state to waiting for a Client ID state
int Client::requestGame()
{
    cout << "Enter game you would like to play:" << endl;
    cout << "(e.g. 1 for tictactoe)" << endl;
    getline(cin, m_game_ID);
    
    // UI: The client shall implement a command line interface

    if (m_game_ID[0] == 'q' || m_game_ID[0] == 'Q') {// quit application
        disconnect();
        return -1;
    }
    
    // Game Type Validation: The client shall send a NEWGAMETYPE message for
    // server validation of the game type contained in the message.

    if(!sent(NEWGAMETYPE, m_game_ID)) {       // Send failed
        cerr << "BGP: Send error in IDLE" << endl;
        return -1;
    }
    
    else {
        cout << "Sent game id: " << m_game_ID << " to server" << endl;
        return ASSIGN_ID;
    }
}

// method parses the Client ID Assign message from the server
// the client id a 32 bit random number assigned by the server to authenticate messages from the client
// the client id is built into the PDU of every message sent by the client, after receipt
// sets the next client state to waiting for an Opponent state
int Client::assignID()
{
    PDU in_pdu;
    
    // Client ID: The client shall accept and store a server generated 32 bit Client ID.

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
                    catch (std::exception& e){
                        cerr << "BGP: Invaid client id type. Must be unsigned int" << endl;
                        return -1;
                    }
                    return FIND_OPP;
                }
                else {
                    cerr << "BGP: No payload received from server in ASSIGN_ID" << endl;
                    return -1;
                }

            default:
                cerr << "BGP: Invalid message type in ASSIGN_ID: " << in_pdu.m_header.m_message_type << endl;
                return -1;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in ASSIGN_ID" << endl; // time out case
        disconnect();
        return -1;
    }
}

// method to parse the Found Opponent message from the server
// the message indicates an opposing player, asking for the same game type, has been found by the server
// the message contains the opponent client id, which is stored for future use
// sets the next client state to Game Start state
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
                    return -1;
                }
            default:
                cerr << "BGP: Invalid message type in FIND_OPP: " << in_pdu.m_header.m_message_type << endl;
                return -1;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in FIND_OPP" << endl; // time out case
        disconnect();
        return -1;
    }
}

// method parses the Player Assigned message from the server, which indicates who is player #1 and player #2
// player #1 always takes the first move, then each player makes a move, swapping back and forth
int Client::assignPlayer()
{
    PDU in_pdu;
    m_gameover = false;
    
    // Player ID: The client shall accept and store a server generated Player ID. Player #1 shall make the first move.

    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case PLAYERASSIGN:
                if(receivedPayload(in_pdu)) { // payload received
                    try {
                        m_player = atoi((char*)in_pdu.m_payload.m_data);
                    }
                    catch (std::exception& e){
                        cerr << "BGP: Invaid player number. Must be a number" << endl;
                        return -1;
                    }
                    
                    return startPosition(m_player);
                }
                else {
                    cerr << "BGP: No payload received from server in GAME_START" << endl;
                    return -1;
                }
            default:
                cerr << "BGP: Invalid message type in GAME_START: " << in_pdu.m_header.m_message_type << endl;
                return -1;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in GAME_START" << endl; // time out case
        disconnect();
        return -1;
    }
}

// method parses the move, sent by the opponent, relayed by the server
// method parses the Invalid Move, Reset, and Game End message, sent by the opponent
// method parses all message the can be received in the client Receive Move state
// sets the next client state to Send Move, Receive Move, or Game Client Reset state
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
                    catch (std::exception& e){
                        cerr << "BGP: Invaid player number. Must be a number" << endl;
                        return -1;
                    }
                    
                    if(m_game.validMove(to_string(m_opp_move), opponent(m_player)))
                        return SEND_MOVE;
                    
                    else {
                        // Invalid Move: The client shall send an invalid move message to the server,
                        // when the move is invalid for the game.
                        if(!sent(INVMOVE, "")) {       // Send failed
                            cerr << "BGP: Send error in RECV_MOVE, INVMOVE message" << endl;
                            return -1;
                        }
                        return RECV_MOVE;
                    }
                }
                else {
                    cerr << "BGP: No payload received from server in RECV_MOVE, MOVE message" << endl;
                    return -1;
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
                    catch (std::exception& e){
                        cerr << "BGP: Invaid reason. Must be a number" << endl;
                        return -1;
                    }
                    m_gameover = true;
                    return GAME_END;
                }
                else {
                    cerr << "BGP: No payload received from server in RECV_MOVE, GAMEEND message" << endl;
                    return -1;
                }
                
            default:
                cerr << "BGP: Invalid message type in RECV_MOVE: " << in_pdu.m_header.m_message_type << endl;
                return -1;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in RECV_MOVE" << endl; // time out case
        disconnect();
        return -1;
    }
}

// method obtains a game move from the player and sends it to the opponent, through the server
// method may obtain a request to end the game or reset the game and sends it to the opponent
// sets the next client state to Game End, Send Move, Receive Move, or Client Game Reset state
int Client::outgoingMove()
{
    // Game Move: The client shall send a game move to the server, when it is the clients turn to move.

    if(!m_game.isGameOver()) {
        if(m_resend_move) {
            if(!sent(MOVE, m_last_move)) {       // Send failed
                cerr << "BGP: Send error in SEND_MOVE, last MOVE message" << endl;
                disconnect();
                return -1;
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
                if(!sent(GAMEEND, to_string(GameEnums::OPPLEFT))) {       // Send failed
                    cerr << "BGP: Send error in SEND_MOVE, GAMEEND message" << endl;
                    disconnect();
                    return -1;
                }
                return GAME_END;
                
            case 'R':
            case 'r':
                if(!sent(RESET, "")) {       // Send failed
                    cerr << "BGP: Send error in SEND_MOVE, RESET message" << endl;
                    disconnect();
                    return -1;
                }
                return SEND_RESET;
                
            default:
                if(m_game.validMove(m_move, m_player)) {
                    m_last_move = m_move;
                    if(!sent(MOVE, m_move)) {       // Send failed
                        cerr << "BGP: Send error in SEND_MOVE, MOVE message" << endl;
                        disconnect();
                        return -1;
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
            return -1;
        }
        return GAME_END;
    }
}

// method parse a response from the opponent to accept or reject a game reset request
// sets the next client state to Game Start or Send Move state
int Client::requestReset()
{
    PDU in_pdu;

    // Reset Game: The client shall send an reset message to the server, when the player request to reset the game.

    cout << "Waiting for reset response from opponent..." << endl;
    
    if(receivedHeader(in_pdu)) { // valid header received
        switch(in_pdu.m_header.m_message_type) {
            case RESETACK:
                return GAME_START;
                
            case RESETNACK:
                return SEND_MOVE;
            
            default:
                cerr << "BGP: Invalid message type in SEND_RESET: " << in_pdu.m_header.m_message_type << endl;
                return -1;
        }
    }
    
    else {
        cerr << "BGP: No message received from server in SEND_RESET" << endl; // time out case
        disconnect();
        return -1;
    }
}

// method to obtain the response to a game reset request from the player
// sends the response to the opponent, through the server
// sets the next client state to Game Start or Receive Move state
int Client::resetResponse()
{
    string response;
    
    cout << "Opponent requested restart" << endl;
    cout << "Accept or Decline [y/n]" << endl;
    getline(cin, response);
    
    switch(response[0]) {
        case 'Y':
        case 'y':
            // Reset Game Acknowledgement: The client shall send an reset ack message to the server,
            // when the player accepts the game reset.
            if(!sent(RESETACK, "")) {       // Send failed
                cerr << "BGP: Send error in RECV_RESET, RESETACK message" << endl;
                disconnect();
                return -1;
            }
            return GAME_START;
        case 'N':
        case 'n':
            // Reset Game Negative Acknowledgement: The client shall send an reset nack message to the server,
            // when the player rejects the game reset.
            if(!sent(RESETNACK, "")) {       // Send failed
                cerr << "BGP: Send error in RECV_RESET, RESETNACK message" << endl;
                disconnect();
                return -1;
            }
            return RECV_MOVE;
        default:
            cout << "Invalid response. Try again." << endl;
            return RECV_RESET;
    }
}

// method to indicate the game is complete to the player
// parses a Game End Acknowledgement from the opponent
// or builds and sends a Game End Acknowledgement to the opponent
// sets the next client state to Idle state
int Client::gameOver()
{
    PDU in_pdu;
    
    // Game End: The client shall send an game end message to the server, when the player ends the game.

    cout << "Gameover: ";
    
    if(!m_gameover) {
        if(receivedHeader(in_pdu)) { // valid header received
            switch(in_pdu.m_header.m_message_type) {
                case GAMEENDACK:
                    cout << reason(m_reason) << endl;
                    return IDLE;
                default:
                    cerr << "BGP: Invalid message type in GAME_END: " << int(in_pdu.m_header.m_message_type) << endl;
                    disconnect();
                    return -1;
            }
        }
        else {
            cerr << "BGP: No message received from server in GAME_END" << endl; // time out case
            disconnect();
            return -1;
        }
    }
        // Game End Acknowledgement: The client shall send an game end acknowledgement message to the server,
        // when the player accepts the game end.
    else {
        m_gameover = false;
        if(!sent(GAMEENDACK, "")) {       // Send failed
            cerr << "BGP: Send error in GAME_END, GAMEENDACK message" << endl;
            return -1;
        }
        cout << reason(m_reason) << endl;
        return IDLE;
    }
}

// display a line to the player
void Client::drawLine()
{
    cout << "----------------------------------------------------" << endl;
}

// indicate to the player, which player number they have been assigned by the server
// sets the next client state to Game Start, Send Move, or Receive Move state
int Client::startPosition(int player)
{
    int result;
    
    switch (player) {
        case GameEnums::PLAYER1:
            cout << "You are player " << (m_player+1) << endl;
            result = SEND_MOVE;
            cout << "When it's your turn, enter 'r' or 'q' to restart or quit current game" << endl;
            break;
        case GameEnums::PLAYER2:
            cout << "You are player " << (m_player+1) << endl;
            result =  RECV_MOVE;
            cout << "When it's your turn, enter 'r' or 'q' to restart or quit current game" << endl;
            break;
        default:
            cout << "BGP: Cannot assign player number: " << player << endl;
            result =  GAME_START;
            break;
    }
    
    return result;
}

// method switches player numbers
int Client::opponent(int player)
{
    switch (player) {
        case GameEnums::PLAYER1:
            return GameEnums::PLAYER2;
        case GameEnums::PLAYER2:
            return GameEnums::PLAYER1;
        default:
            cout << "BGP: Cannot return opponent number: " << player << endl;
            return player;
    }
}

// method provides the reason the game is ending for display to the player
string Client::reason(int r)
{
    switch(r) {
        case GameEnums::GAMEOVER:
            return "Gameplay has finished";
        case GameEnums::OPPLEFT:
            return "Opponent ended the game";
        case GameEnums::QUIT:
            return "You ended the game";
        default:
            cout << "BGP: Invalid game end reason: " << r << endl;
            return "";
    }
}

// method to disconnect from the server
// provide an indication to the player, the server is disconnected
void Client::disconnect()
{
    cout << "Disconnecting from " << m_server_address << " on port " << m_port << "..." << endl;
    shutdown(m_sock, SHUT_RDWR);
    close(m_sock);
}

// method to create a client socket and connect to the server
// provide an indication to the player, the server is connected
// displays confirmation and error message to the player
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
        
        cerr << "Socket created" << endl;
    }
    else    {   /* OK , nothing */  }
    
    // IP and hostname: Client shall be able to specify the hostname and/or the IP address of the server.

    if(address.find(".") == string::npos || address.length() > 15) { // hostname
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

// method to lookup an IP address from a hostname
// displays error message to the player
string Client::lookupHostname(string hostname)
{
    struct hostent *he;
    struct in_addr **addr_list;
    
    if ( (he = gethostbyname( hostname.c_str() ) ) == NULL)
    {
        // get the host info
        perror("gethostbyname failed");
        return hostname;
    }
    
    addr_list = (struct in_addr **) he->h_addr_list;
    
    return string(inet_ntoa(*addr_list[0]));
}

// helper method to build and send PDUs to the server
// displays error message to the player
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

// helper method to receive a header only PDU from the server and validate the PDU header
// displays error message to the player
bool Client::receivedHeader(const PDU &in_pdu)
{
    unsigned char buffer[8]; // fixed header size
    
    if(recv(m_sock, buffer, 8, 0) < 0) {
        cerr << "Receive header failed" << endl;
        return false;
    }
    
    memcpy((char *)&in_pdu.m_header, buffer, 8);
    
    // PDU Validation: The client shall validate the protocol version, message type,
    // and client ID of all messages received.

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

// helper method to receive a PDU from the server and extract the payload
// displays error message to the player
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