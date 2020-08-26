#include "Sender.h"

Define_Module(Sender);

void Sender::initialize()
{
    beep = new cMessage("beep");

    rate = 1/par("lambda").doubleValue();

    double time = exponential(rate);
    scheduleAt(simTime() + time, beep);
}

Packet* Sender::generatePacket()
{
    Packet *packet = new Packet(getName());

    int maxDim = getParentModule()->par("MAXIMUM_PACKET_SIZE").intValue();

    packet->setSize(intuniform(0, maxDim));

    return packet;
}

void Sender::handleMessage(cMessage *msg)
{
    if(msg->isSelfMessage())
    {
        Packet *packet = generatePacket();

        send(packet, "out");

        double time = exponential(rate);
        scheduleAt(simTime() + time, beep);
    }
}
