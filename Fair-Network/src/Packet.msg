cplusplus{{
	#include <vector>
	typedef std::vector<int> IntVector;
}}

class noncobject IntVector;

packet Packet {
    int size;
    int destination;
    IntVector RBs;
}
