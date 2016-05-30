//
//  pdu.cpp
//  tictactoe
//
//  Created by TJ Rhodes on 5/28/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#include "pdu.hpp"

using namespace PDUEnums;

PDU::PDU()
{
    m_header.m_version = 1;
    m_header.m_length = 0;
    m_header.m_reserved = 0;
    
}

PDU::~PDU()
{
}


void PDU::buildPDU(unsigned int id, int message, string data)
{
    this->m_header.m_client_ID = id;
    unsigned char prep_data[data.length()];
    data.copy((char*)prep_data, data.length(), 0);
    
    switch(message) {
        case NEWGAMETYPE:
            this->m_header.m_message_type = NEWGAMETYPE;
            memcpy(&this->m_payload.m_data, prep_data, data.length());
            this->m_header.m_length = data.length();
            break;
        case MOVE:
            this->m_header.m_message_type = MOVE;
            memcpy(&this->m_payload.m_data, prep_data, data.length());
            this->m_header.m_length = data.length();
            break;
        case INVMOVE:
            this->m_header.m_message_type = INVMOVE;
            break;
        case RESET:
            this->m_header.m_message_type = RESET;
            break;
        case RESETACK:
            this->m_header.m_message_type = RESETACK;
            break;
        case RESETNACK:
            this->m_header.m_message_type = RESETNACK;
            break;
        case GAMEEND:
            this->m_header.m_message_type = GAMEEND;
            break;
        case GAMEENDACK:
            this->m_header.m_message_type = GAMEENDACK;
            break;
        default:
            this->m_header.m_version = -1; // bad message
    }
}