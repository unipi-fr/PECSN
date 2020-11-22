#include "User.h"

Define_Module(User);

void User::initialize()
{
    id = getIndex();

    int numUser = getParentModule()->par("NUM_USER").intValue();
    indexRNGCQI = id+2*numUser;

    double mean = 15.0/numUser * (id+1);
    p = mean/15; //n = 15; da 0 a 14
    EV<< "Mean: " << mean << "   " << "P:" << p << endl;
    simDelay = registerSignal("packetDelay");
    simThroughput = registerSignal("userThroughput");
    simThroughputTotal = registerSignal("userThroughputTotal");
    simUserSelectedTotal = registerSignal("userSelected");

    userSelectedCount = 0;
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
    bool aPacketBelongToMe = false;
    while(packets.size() != 0){
        Packet* currentPacket = packets.back();
        packets.pop_back();

        if(currentPacket->getDestination() == id){
            aPacketBelongToMe = true;
            collectStatistics(currentPacket);
            bytesReceivedFrame += currentPacket->getSize();
        }
    }

    if (aPacketBelongToMe){
        ++userSelectedCount;
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
        cqi = binomial(14, p, indexRNGCQI);
            cqi += 1; // cqi must be within [1, 15]
    }else{
        cqi = intuniform(1, 15, indexRNGCQI);
    }
    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);

    send(cqiMsg, "out");
}

void User::finish()
{
    emit(simThroughputTotal, byteReceived/(simTime()-warmUp));
    emit(simUserSelectedTotal, userSelectedCount);
}

