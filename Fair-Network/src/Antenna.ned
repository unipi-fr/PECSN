package fair_network;

simple Antenna
{
    parameters:
        double timeSlot @unit(s) = default(1s);
        
    gates:
        input packetIn;
        
        input in[];
        output out[];
}
