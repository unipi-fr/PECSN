#include "Antenna.h"

Define_Module(Antenna);

void Antenna::initialize()
{

    CQITable = new int[15];
    CQITable[0] = 3;
    CQITable[1] = 3;
    CQITable[2] = 6;
    CQITable[3] = 11;
    CQITable[4] = 15;
    CQITable[5] = 20;
    CQITable[6] = 25;
    CQITable[7] = 36;
    CQITable[8] = 39;
    CQITable[9] = 50;
    CQITable[10] = 63;
    CQITable[11] = 72;
    CQITable[12] = 80;
    CQITable[13] = 93;
    CQITable[14] = 93;

    beep = new cMessage("Beep");
    frame = new Frame("Frame");

    int nQueues = getParentModule()->par("NUM_USER");

    queuesOrderedByUser = new UserQueue*[nQueues];
    queuesOrderedByBytesSent = new cQueue("Queues");

    queuesOrderedByBytesSent->setup(UserQueue::compareUserQueue);

    for(int i = 0; i < nQueues; i++)
    {
        std::string name = "User" + std::to_string(i);
        queuesOrderedByUser[i] = new UserQueue(name.c_str());
        queuesOrderedByUser[i]->RBsize = 20;
        queuesOrderedByBytesSent->insert(queuesOrderedByUser[i]);
    }

    scheduleAt(simTime() + par("timeSlot").doubleValue(), beep);
}

bool Antenna::loadPacketIntoFrame(Frame *frame, UserQueue *userQueue)
{
    int RBused = frame->getRBused();
    std::vector<Packet*> packetsVector = frame->getPackets();
    int RBsize = userQueue->RBsize;

    int RBfree;
    int freeSpace;
    int freeBytesFromLastRB = 0;
    int packetSize;
    Packet* currentPacket;

    while(!userQueue->isEmpty()){
        RBfree = 25-RBused;
        freeSpace = RBfree*RBsize;
        currentPacket = check_and_cast<Packet*>(userQueue->get(0));
        packetSize = currentPacket->getSize();
        //if packet doesn't fit into frame
        if(packetSize > freeSpace + freeBytesFromLastRB){
            //check if frame is full
            if(RBfree == 0){
                //update frame packets vector
                frame->setPackets(packetsVector);
                //notify that frame is ready
                return true;
            }
            break;
        }

        //then calculate the RB occupied from packet, remembering the free space from last RB
        float RBoccupiedFromPacket = ((float)(packetSize-freeBytesFromLastRB))/RBsize;
        //get the RBs of the packet to be updated
        std::vector<int> RBs = currentPacket->getRBs();
        //check if were free space from last RB
        if(freeBytesFromLastRB > 0)
            //assign packet at that RB
            RBs.push_back(RBused);
        //check if are other RBs
        if(RBoccupiedFromPacket > 0){
            //calculate how many RBs are missing
            int RBoccupied = std::ceil(RBoccupiedFromPacket);
            for(int i = 0; i<RBoccupied; ++i){
                //i add those RBs to RBs vector of the packet
                RBs.push_back(++RBused);
            }
            //calculate free bytes of last RB
            freeBytesFromLastRB = (RBsize - ((packetSize - freeBytesFromLastRB) % RBsize)) ;
        }else{
            //if was complitelly in the last RB i remove from lastRB the packet size
            freeBytesFromLastRB -= packetSize;
        }
        //update the RBs of the current packet
        currentPacket->setRBs(RBs);
        //update RBs used of the frame
        frame->setRBused(RBused);
        //insert current packet into frame
        packetsVector.push_back(currentPacket);
        //remove current packet from queue
        userQueue->remove(currentPacket);
        //update byte sent of that queue
        userQueue->byteSent += packetSize;
    }

    //update frame packets vector
    frame->setPackets(packetsVector);
    //check if frame is full
    if(RBfree == 0)
        //notify that frame is ready
        return true;
    //the frame has free RBs after elaborating this user queue
    return false;
}

void Antenna::clearFrame(){
    frame->setRBused(0);
    std::vector<Packet*> packets = frame->getPackets();
    while(packets.size() != 0){
        Packet* currentPacket = packets.back();
        packets.pop_back();
        delete(currentPacket);
    }
    frame->setPackets(packets);
}

void Antenna::prepareFrame()
{
    clearFrame();

    int nQueues = getParentModule()->par("NUM_USER");

    std::vector<UserQueue*> indexQueue;

    bool isReady = false;
    for(int i = 0; i < nQueues && !isReady; i++)
    {
        UserQueue *uq = check_and_cast<UserQueue*>(queuesOrderedByBytesSent->get(i));

        if(uq->isEmpty())
            continue;

        indexQueue.push_back(uq); // indexQueue contains index of queue to remove and to reinsert

        isReady = loadPacketIntoFrame(frame, uq);
    }

    for(int i = 0; i < indexQueue.size(); i++)
    {
        UserQueue *uq = indexQueue[i];
        queuesOrderedByBytesSent->remove(uq);

        queuesOrderedByBytesSent->insert(uq);
    }

    indexQueue.clear();
}

void Antenna::sendFrame(cMessage *msg)
{
    prepareFrame();

    int nUser= getParentModule()->par("NUM_USER").intValue();
    for(int i=0; i<nUser; ++i){
        Frame *f = new Frame(*frame);
        send(f, "out", i);
    }

    scheduleAt(simTime() + par("timeSlot").doubleValue(), beep);
}

void Antenna::savePacket(cMessage *msg)
{
    Packet *packet = check_and_cast<Packet*>(msg);

    EV_INFO<<packet->getName()<<" size: "<<packet->getSize()<<" "<<packet->getDestination();

    packet->setArrivalTime(simTime());

    queuesOrderedByUser[packet->getDestination()]->insert(packet);
}

void Antenna::updateCQI(cMessage *msg)
{
    int destination = msg->getArrivalGate()->getIndex();

    CqiMsg *cqiMsg = check_and_cast<CqiMsg*>(msg);

    int index = cqiMsg->getValue()-1; // -1 because we saved the cqiTable starting from 0 instead of 1
    UserQueue *uq = queuesOrderedByUser[destination];

    uq->RBsize = CQITable[index];

    delete(cqiMsg);
}

void Antenna::handleMessage(cMessage *msg)
{
    if(msg->isSelfMessage())
    {
        sendFrame(msg);
    }

    if(strcmp(msg->getName(),"Packet") == 0)
    {
        savePacket(msg);
    }

    if(strcmp(msg->getName(),"CQI") == 0)
    {
        updateCQI(msg);
    }

}
