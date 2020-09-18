package fair_network.simulations;

import fair_network.Antenna;
import fair_network.User;
import fair_network.PacketGenerator;

network FairNetwork
{
    parameters:
        int NUM_USER = default(2);
        double TIMESLOT @unit(ms) = default(1000ms); 
        double WARMUP @unit(ms) = default(0ms);
        
    submodules:
        antenna: Antenna{
            timeSlot = TIMESLOT;
        }
        user[NUM_USER]: User;
        packetGenerator: PacketGenerator{
        	NUM_SENDERS = NUM_USER;
        }
        
    connections:
        
        for i=0..NUM_USER-1 {
            antenna.out++ --> user[i].in;
            antenna.in++ <-- user[i].out;
        }
        
        packetGenerator.out --> antenna.packetIn;
}
