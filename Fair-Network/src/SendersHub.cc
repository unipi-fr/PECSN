#include "SendersHub.h"

Define_Module(SendersHub);

void SendersHub::initialize()
{
    simProduced = registerSignal("bytesProduced");

    int numUser = getParentModule()->getParentModule()->par("NUM_USER").intValue();

    senderBytesProduced = new int[numUser];
    for(int i = 0; i<numUser; i++)
        senderBytesProduced[i] = 0;
}

void SendersHub::handleMessage(cMessage *msg)
{
    int destination = msg->getArrivalGate()->getIndex();

    Packet *packet = check_and_cast<Packet*>(msg);
    senderBytesProduced[destination] += packet->getSize();

    packet->setDestination(destination);

    send(packet, "out");
}

void SendersHub::finish(){
    int numUser = getParentModule()->getParentModule()->par("NUM_USER").intValue();

    for(int i = 0; i < numUser; i++){
        emit(simProduced, senderBytesProduced[i]/simTime());
    }

    delete[] senderBytesProduced;
}
