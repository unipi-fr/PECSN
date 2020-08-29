#include "User.h"

Define_Module(User);

void User::initialize()
{

    id = getIndex();

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
            //delete(currentPacket);
        }
    }

    delete(msg);

    sendCQI();
}

void User::collectStatistics(Packet* packet){

}

void User::sendCQI() {
    cqi = intuniform(1, 15);
    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);
    send(cqiMsg, "out");
}
