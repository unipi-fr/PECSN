package fair_network.simulations;

import fair_network.Antenna;
import fair_network.User;
import fair_network.PacketGenerator;

network FairNetwork
{
    submodules:
        antenna: Antenna;
        user1: User;
        user2: User;
        packetGenerator: PacketGenerator; 
        
    connections:
        antenna.out++ --> user1.in;
        antenna.out++ --> user2.in;
        
        antenna.in++ <-- user1.out;
        antenna.in++ <-- user2.out;
        
        packetGenerator.out --> antenna.packetIn;
}
