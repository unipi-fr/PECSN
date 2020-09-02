package fair_network;

simple Antenna
{
    parameters:
        double timeSlot @unit(ms) = default(1000ms);
        
    gates:
        input packetIn;
        
        input in[];
        output out[];
}
