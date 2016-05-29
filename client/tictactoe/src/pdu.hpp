//
//  pdu.hpp
//  tictactoe
//
//  Created by TJ Rhodes on 5/28/16.
//  Copyright © 2016 BGP Protocol. All rights reserved.
//

#ifndef pdu_hpp
#define pdu_hpp

#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct pduHeader {
    unsigned char m_version;
    unsigned char m_message_type;
    unsigned char m_length;
    unsigned char m_reserved;
    unsigned long m_client_ID;
};

struct pduPayload {
    unsigned char m_data[1016];
};

class PDU
{
public:
    PDU();
    ~PDU();
    
public:
    
    pduHeader m_header;
    pduPayload m_payload;
    
    void buildPDU(unsigned long id, int message, unsigned char * data);
    
};

namespace PDUEnums
{
    enum Messages {
                    NEWGAMETYPE,
                    INVGAMETYPE,
                    CLIENTIDASSIGN,
                    FOUNDOPP,
                    PLAYERASSIGN,
                    MOVE,
                    INVMOVE,
                    RESET,
                    RESETACK,
                    RESETNACK,
                    GAMEEND,
                    GAMEENDACK
    };
}

#endif /* pdu_hpp */
