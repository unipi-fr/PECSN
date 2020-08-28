cplusplus{{
	#include <vector>
	#include "Packet_m.h"
	
	typedef std::vector<Packet *> PacketVector;
}}

class noncobject PacketVector;

packet Frame {
    int RBused;
    PacketVector packets;
}
