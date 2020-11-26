#ifndef __FAIR_NETWORK_SENDERSHUB_H_
#define __FAIR_NETWORK_SENDERSHUB_H_

#include <omnetpp.h>
#include "Packet_m.h"

using namespace omnetpp;

class SendersHub : public cSimpleModule
{
  private:
    simsignal_t simProduced;

    int* senderBytesProduced;

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
    virtual void finish();
};

#endif
