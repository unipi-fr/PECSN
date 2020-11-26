#include "Sender.h"

Define_Module(Sender);

void Sender::initialize()
{
    beep = new cMessage("beep");

    mean = 1/par("lambda").doubleValue();

    int numUser = getParentModule()->getParentModule()->par("NUM_USER").intValue();
    indexRNGExp = getIndex()+0*numUser;
    indexRNGUnif = getIndex()+1*numUser;

    double time = exponential(mean, indexRNGExp);
    scheduleAt(simTime() + time, beep);
}

Packet* Sender::generatePacket()
{
    Packet *packet = new Packet("Packet");

    int maxDim = getParentModule()->par("MAXIMUM_PACKET_SIZE").intValue();

    int size = intuniform(1, maxDim, indexRNGUnif);
    packet->setSize(size);

    return packet;
}

void Sender::handleMessage(cMessage *msg)
{
    if(msg->isSelfMessage())
    {
        Packet *packet = generatePacket();

        send(packet, "out");

        double time = exponential(mean, indexRNGExp);
        //EV<<"Time = "<<time<<endl;
        scheduleAt(simTime() + time, beep);
    }
}

