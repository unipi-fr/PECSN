package fair_network;

module PacketGenerator
{
	parameters:
        int MAXIMUM_PACKET_SIZE = default(75);
        
    gates:
        output out;
    
    submodules:
        sender1: Sender{
        	id = 1;
        }
        
        sender2: Sender{
        	id = 2;
        }
        
        hub: SendersHub;
        
        connections:
        	sender1.out --> hub.in++;
        	sender2.out --> hub.in++;
        	
        	hub.out --> out;
}
