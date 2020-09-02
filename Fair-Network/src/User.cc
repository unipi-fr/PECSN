#include "User.h"

Define_Module(User);

void User::initialize()
{
    id = getIndex();

    int numUser = getParentModule()->par("NUM_USER").intValue();
    indexRNGCQI = id+2*numUser;

    int mean = 14/numUser * (id+1); //14 for not reach 15
    p = mean/15; //n = 15;

    simDelay = registerSignal("packetDelay");
    simBytes = registerSignal("packetBytes");
    simThroughput = registerSignal("userThroughput");

    timeSlot = getParentModule()->par("TIMESLOT").doubleValueInUnit("s");

    sendCQI();
}

void User::handleMessage(cMessage *msg)
{
    // getting the frame
    Frame *frame = check_and_cast<Frame*>(msg);

    std::vector<Packet*> packets = frame->getPackets();

    //search for packets with this user destination
    long bytesReceived = 0;
    while(packets.size() != 0){
        Packet* currentPacket = packets.back();
        packets.pop_back();

        if(currentPacket->getDestination() == id){
            collectStatistics(currentPacket);
            bytesReceived += currentPacket->getSize();
        }
    }

    emit(simThroughput,bytesReceived/timeSlot);

    delete(msg);

    sendCQI();
}

void User::collectStatistics(Packet* packet){
    long size = packet->getSize();
    simtime_t timeToDeliver = simTime() - packet->getArrivalTime();
    emit(simDelay,timeToDeliver);
    emit(simBytes,size);
}

void User::sendCQI() {
    if(par("useBinomialDistribution").boolValue()){
        cqi = binomial(15, p, indexRNGCQI);
    }else{
        cqi = intuniform(1, 15, indexRNGCQI);
    }
    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);
    send(cqiMsg, "out");
}
