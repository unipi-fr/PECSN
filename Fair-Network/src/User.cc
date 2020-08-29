#include "User.h"

Define_Module(User);

void User::initialize()
{
    cqi = intuniform(1, 15);

    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);

    send(cqiMsg, "out");
}

void User::handleMessage(cMessage *msg)
{
    // leggere pacchetti inviati nel frame per vedere se ce n'e' uno per questo utente

    delete(msg);

    cqi = intuniform(1, 15);

    CqiMsg *cqiMsg = new CqiMsg("CQI");
    cqiMsg->setValue(cqi);

    send(cqiMsg, "out");
}
