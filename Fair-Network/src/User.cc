#include "User.h"

Define_Module(User);

void User::initialize()
{
    id = getIndex();

    simDelay = registerSignal("packetDelay");

    sendCQI();
}

void User::handleMessage(cMessage *msg)
{
    // getting the frame
    Frame *frame = check_and_cast<Frame*>(msg);

    std::vector<Packet*> packets = frame->getPackets();

    //search for packets with this user destination
    while(packets.size() != 0){
        Packet* currentPacket = packets.back();
        packets.pop_back();

        if(currentPacket->getDestination() == id){
            collectStatistics(currentPacket);
        }
    }

    delete(msg);

    sendCQI();
}

void User::collectStatistics(Packet* packet){
    simtime_t timeToDeliver = simTime() - packet->getArrivalTime();
    emit(simDelay,timeToDeliver);
    EV_TRACE<< packet->info()<<"delivered in "<<timeToDeliver<<endl;
}

void User::sendCQI() {
    cqi = intuniform(1, 15);
    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);
    send(cqiMsg, "out");
}
