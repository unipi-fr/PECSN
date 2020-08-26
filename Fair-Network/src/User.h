#ifndef __FAIR_NETWORK_USER_H_
#define __FAIR_NETWORK_USER_H_

#include <omnetpp.h>

using namespace omnetpp;

class User : public cSimpleModule
{
  protected:
    virtual void initialize();
    virtual void handleMessage(cMessage *msg);
  private:
  

};

#endif
