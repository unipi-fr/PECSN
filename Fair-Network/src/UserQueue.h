#ifndef USERQUEUE_H_
#define USERQUEUE_H_

#include <omnetpp.h>

class UserQueue: public omnetpp::cQueue{
  public:
    int RBsize;
    int index;
    long byteSent;
    int selectedUserCount;

    UserQueue(const char *name);
    virtual ~UserQueue();

    void userSelected();
    int getSelectedUserCount();
    static int compareUserQueue(cObject *a, cObject *b);
};

#endif
