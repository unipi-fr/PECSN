#ifndef __FAIR_NETWORK_ANTENNA_H_
#define __FAIR_NETWORK_ANTENNA_H_

#include <omnetpp.h>
#include <vector>
#include "Packet_m.h"
#include "UserQueue.h"
#include "Frame_m.h"
#include "CqiMsg_m.h"
#include <math.h>

using namespace omnetpp;

class Antenna : public cSimpleModule
{
  private:
    simsignal_t simQueue;
    simsignal_t simFrame;

    cMessage *beep;
    Frame *frame;

    UserQueue** queuesOrderedByUser;
    cQueue *queuesOrderedByBytesSent;

    int *CQITable;

    void prepareFrame();
    void clearFrame();
    bool loadPacketIntoFrame(Frame *frame, UserQueue *userQueue);
    void sendFrame(cMessage *msg);
    void savePacket(cMessage *msg);
    void updateCQI(cMessage *msg);
    void scheduleBeep();
    void collectStatistics();

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
};

#endif
