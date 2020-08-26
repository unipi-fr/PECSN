package fair_network;

module PacketGenerator
{
	parameters:
        int MAXIMUM_PACKET_SIZE = default(75);
        int NUM_SENDERS = default(2);
        
    gates:
        output out;
    
    submodules:
        senders[NUM_SENDERS]: Sender;
        
        hub: SendersHub;
        
        connections:
        	for i = 0..NUM_SENDERS-1 {
        		senders[i].out --> hub.in++;   
        	}
        	
        	hub.out --> out;
}
