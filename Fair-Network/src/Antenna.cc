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
        queuesOrderedByBytesSent->insert(queuesOrderedByUser[i]);
    }

    scheduleAt(simTime() + par("timeSlot").doubleValue(), beep);
}

void Antenna::loadPacketIntoFrame(Frame *frame, UserQueue *userQueue)
{
    // TO DO;
}

Frame* Antenna::prepareFrame()
{
    Frame* frame = new Frame("Frame");

    int nQueues = getParentModule()->par("NUM_USER");

    std::vector<int> indexQueue;

    for(int i = 0; i < nQueues; i++)
    {
        UserQueue *uq = check_and_cast<UserQueue*>(queuesOrderedByBytesSent->get(i));

        if(uq->isEmpty())
            continue;

        indexQueue.push_back(i); // indexQueue contains index of queue to remove and to reinsert

        loadPacketIntoFrame(frame, uq);
    }

    for(int i = 0; i < indexQueue.size(); i++)
    {
        UserQueue *uq = queuesOrderedByBytesSent->get(indexQueue[i]);
        queuesOrderedByBytesSent->remove(uq);

        queuesOrderedByBytesSent->insert(uq);
    }

    return frame;
}

void Antenna::handleMessage(cMessage *msg)
{
    if(msg->isSelfMessage())
    {

    } else {
        Packet *packet = check_and_cast<Packet*>(msg);

        EV_INFO<<packet->getName()<<" size: "<<packet->getSize()<<" "<<packet->getDestination();

        queuesOrderedByUser[packet->getDestination()]->insert(msg);
    }

}
