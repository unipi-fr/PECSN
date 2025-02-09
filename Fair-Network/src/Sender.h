#ifndef __FAIR_NETWORK_SENDER_H_
#define __FAIR_NETWORK_SENDER_H_

#include <omnetpp.h>
#include "Packet_m.h"

using namespace omnetpp;

class Sender : public cSimpleModule
{
  private:
    double mean;
    cMessage *beep;

    int indexRNGExp;
    int indexRNGUnif;

    Packet* generatePacket();

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

#endif
