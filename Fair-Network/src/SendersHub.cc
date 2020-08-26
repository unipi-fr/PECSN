#include "SendersHub.h"

Define_Module(SendersHub);

void SendersHub::initialize()
{

}

void SendersHub::handleMessage(cMessage *msg)
{
    send(msg, "out");
}
