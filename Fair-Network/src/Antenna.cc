#include "Antenna.h"

Define_Module(Antenna);

void Antenna::initialize()
{
    beep = new cMessage("Beep");

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
        //prendere la dimensione del pachetto
        packetSize = currentPacket->getSize();
        //se non ci stà mi fermo e passerò al prossimo utente
        if(packetSize > freeSpace + freeBytesFromLastRB){
            if(RBfree == 0){
                frame->setPackets(packetsVector);
                return true;
            }
            break;
        }

        //calcolo quanti RB occupa, tenendo conto dell'esubero del precedente
        float RBoccupiedFromPacket = ((float)(packetSize-freeBytesFromLastRB))/RBsize;
        std::vector<int> RBs = currentPacket->getRBs();
        //completo il pachetto rpecedente
        if(freeBytesFromLastRB > 0)
            RBs.push_back(RBused);
        //calcolo i rimanenti
        if(RBoccupiedFromPacket > 0){
            int RBoccupied = std::ceil(RBoccupiedFromPacket);
            for(int i = 0; i<RBoccupied; ++i){
                RBs.push_back(++RBused);
            }
            //aggiorno quello del frame
            frame->setRBused(RBused);
            //ricalcolo i bytes liberi nell'ultimo frame
            freeBytesFromLastRB = (RBsize - ((packetSize - freeBytesFromLastRB) % RBsize)) ;
        }
        currentPacket->setRBs(RBs);

        packetsVector.push_back(currentPacket);
        userQueue->remove(currentPacket);
        userQueue->byteSent += packetSize;

    }

    frame->setPackets(packetsVector);
    //at the end of the queue the frame is not completed
    return false;
}

Frame* Antenna::prepareFrame()
{
    Frame* frame = new Frame("Frame");
    frame->setRBused(0);

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
    return frame;
}

void Antenna::handleMessage(cMessage *msg)
{
    if(msg->isSelfMessage())
    {
        Frame *frame = prepareFrame();

        int nUser= getParentModule()->par("NUM_USER").intValue();
        for(int i=0; i<nUser; ++i){
            Frame *f = new Frame(*frame);
            send(f, "out", i);
        }

        scheduleAt(simTime() + par("timeSlot").doubleValue(), beep);
    } else {
        Packet *packet = check_and_cast<Packet*>(msg);

        EV_INFO<<packet->getName()<<" size: "<<packet->getSize()<<" "<<packet->getDestination();

        queuesOrderedByUser[packet->getDestination()]->insert(msg);
    }

}
