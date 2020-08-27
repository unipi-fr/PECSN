#include "SendersHub.h"

Define_Module(SendersHub);

void SendersHub::initialize()
{

}

void SendersHub::handleMessage(cMessage *msg)
{
    int destination = msg->getArrivalGate()->getIndex();

    Packet *packet = check_and_cast<Packet*>(msg);
    packet->setDestination(destination);

    send(packet, "out");
}
