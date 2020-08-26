#ifndef __FAIR_NETWORK_SENDERSHUB_H_
#define __FAIR_NETWORK_SENDERSHUB_H_

#include <omnetpp.h>
#include "Packet_m.h"

using namespace omnetpp;

class SendersHub : public cSimpleModule
{
  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

#endif
