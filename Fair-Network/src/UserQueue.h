#ifndef USERQUEUE_H_
#define USERQUEUE_H_

#include <omnetpp.h>

class UserQueue: public omnetpp::cQueue{
  public:
    long byteSent;

    UserQueue(const char *name);
    virtual ~UserQueue();

    static int compareUserQueue(cObject *a, cObject *b);
};

#endif
