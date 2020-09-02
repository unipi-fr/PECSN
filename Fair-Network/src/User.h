#ifndef __FAIR_NETWORK_USER_H_
#define __FAIR_NETWORK_USER_H_

#include <omnetpp.h>
#include <vector>
#include "CqiMsg_m.h"
#include "Frame_m.h"
#include "Packet_m.h"

using namespace omnetpp;

class User : public cSimpleModule
{
  private:
    simsignal_t simDelay;
    simsignal_t simBytes;
    simsignal_t simThroughput;
    int cqi;
    int id;
    double timeSlot;

    int indexRNGCQI;

    void collectStatistics(Packet* packet);
    void sendCQI();

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
  private:
  

};

#endif
