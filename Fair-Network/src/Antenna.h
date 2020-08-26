#ifndef __FAIR_NETWORK_ANTENNA_H_
#define __FAIR_NETWORK_ANTENNA_H_

#include <omnetpp.h>
#include "Packet_m.h"

using namespace omnetpp;

class Antenna : public cSimpleModule
{
  private:
    cMessage *beep;

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

#endif
