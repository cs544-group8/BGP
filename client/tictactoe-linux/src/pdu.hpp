//  CS544 - Computer Networks
//  Group 8
//  Copyright © 2016 BGP Protocol
//  Team Members: Ryan Mann, Brian Quinn, TJ Rhodes, Marc Thomson
//
//  File name: pdu.hpp
//  Description: header file for pdu object

#ifndef pdu_hpp
#define pdu_hpp

#include <stdio.h>
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

// PDU header structure
struct pduHeader {
    unsigned char m_version;
    unsigned char m_message_type;
    unsigned char m_length;
    unsigned char m_reserved;
    unsigned int m_client_ID;
};

// PDU payload structure
struct pduPayload {
    unsigned char m_data[1016];
};

// PDU class that contains a PDU header and PDU payload
// contains the class attributes and method prototypes
class PDU
{
public:
    PDU();
    ~PDU();
    
public:
    
    pduHeader m_header;
    pduPayload m_payload;
    
    void buildPDU(unsigned int id, int message, string data);
    
};

// PDU message types enumeration
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
