#include "Antenna.h"

Define_Module(Antenna);

void Antenna::initialize()
{
    beep = new cMessage("Beep");
}

void Antenna::handleMessage(cMessage *msg)
{
    Packet *packet = check_and_cast<Packet*>(msg);

    EV_INFO<<packet->getName()<<" size: "<<packet->getSize()<<" "<<packet->getDestination();
}
