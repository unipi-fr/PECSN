#ifndef __FAIR_NETWORK_ANTENNA_H_
#define __FAIR_NETWORK_ANTENNA_H_

#include <omnetpp.h>
#include <vector>
#include "Packet_m.h"
#include "UserQueue.h"
#include "Frame_m.h"
#include <math.h>

using namespace omnetpp;

class Antenna : public cSimpleModule
{
  private:
    cMessage *beep;

    UserQueue** queuesOrderedByUser;
    cQueue *queuesOrderedByBytesSent;

    Frame* prepareFrame();
    bool loadPacketIntoFrame(Frame *frame, UserQueue *userQueue);

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

#endif
