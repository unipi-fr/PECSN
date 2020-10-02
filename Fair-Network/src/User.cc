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
    simThroughput = registerSignal("userThroughput");
    simThroughputTotal = registerSignal("userThroughputTotal");

    byteReceived = 0;

    timeSlot = getParentModule()->par("TIMESLOT").doubleValueInUnit("s");
    warmUp = getParentModule()->par("WARMUP").doubleValueInUnit("s");

    sendCQI();
}

void User::handleMessage(cMessage *msg)
{
    // getting the frame
    Frame *frame = check_and_cast<Frame*>(msg);

    std::vector<Packet*> packets = frame->getPackets();

    //search for packets with this user destination
    long bytesReceivedFrame = 0;
    while(packets.size() != 0){
        Packet* currentPacket = packets.back();
        packets.pop_back();

        if(currentPacket->getDestination() == id){
            collectStatistics(currentPacket);
            bytesReceivedFrame += currentPacket->getSize();
        }
    }

    emit(simThroughput,bytesReceivedFrame/timeSlot);

    if(simTime() >= warmUp)
        byteReceived += bytesReceivedFrame;

    delete(msg);

    sendCQI();
}

void User::collectStatistics(Packet* packet){
    simtime_t timeToDeliver = simTime() - packet->getArrivalTime();
    emit(simDelay,timeToDeliver);
}

void User::sendCQI() {
    if(par("useBinomialDistribution").boolValue()){
        cqi = binomial(15, p, indexRNGCQI);
    }else{
        cqi = intuniform(1, 15, indexRNGCQI);
        cqi = 15;
    }
    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);
    send(cqiMsg, "out");
}

void User::finish()
{
    emit(simThroughputTotal, byteReceived/(simTime()-warmUp));
}

