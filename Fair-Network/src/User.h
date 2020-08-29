#ifndef __FAIR_NETWORK_USER_H_
#define __FAIR_NETWORK_USER_H_

#include <omnetpp.h>
#include "CqiMsg_m.h"

using namespace omnetpp;

class User : public cSimpleModule
{
  private:
    int cqi;

  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
  private:
  

};

#endif
