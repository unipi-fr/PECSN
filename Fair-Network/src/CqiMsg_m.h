//
// Generated file, do not edit! Created by nedtool 5.6 from CqiMsg.msg.
//

#ifndef __CQIMSG_M_H
#define __CQIMSG_M_H

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wreserved-id-macro"
#endif
#include <omnetpp.h>

// nedtool version check
#define MSGC_VERSION 0x0506
#if (MSGC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of nedtool: 'make clean' should help.
#endif



/**
 * Class generated from <tt>CqiMsg.msg:1</tt> by nedtool.
 * <pre>
 * packet CqiMsg
 * {
 *     int value;
 * }
 * </pre>
 */
class CqiMsg : public ::omnetpp::cPacket
{
  protected:
    int value;

  private:
    void copy(const CqiMsg& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const CqiMsg&);

  public:
    CqiMsg(const char *name=nullptr, short kind=0);
    CqiMsg(const CqiMsg& other);
    virtual ~CqiMsg();
    CqiMsg& operator=(const CqiMsg& other);
    virtual CqiMsg *dup() const override {return new CqiMsg(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const override;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b) override;

    // field getter/setter methods
    virtual int getValue() const;
    virtual void setValue(int value);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const CqiMsg& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, CqiMsg& obj) {obj.parsimUnpack(b);}


#endif // ifndef __CQIMSG_M_H

