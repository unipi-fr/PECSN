#include "UserQueue.h"

int UserQueue::compareUserQueue(cObject *a, cObject *b) {
    UserQueue *ua = omnetpp::check_and_cast<UserQueue*>(a);
    UserQueue *ub = omnetpp::check_and_cast<UserQueue*>(b);

    if(ua->byteSent < ub->byteSent)
        return -1;

    if(ua->byteSent == ub->byteSent)
        return 0;

    return 1;
}

UserQueue::UserQueue(const char *name):cQueue(name) {
    byteSent = 0;
}

UserQueue::~UserQueue() {
    // TODO Auto-generated destructor stub
}

