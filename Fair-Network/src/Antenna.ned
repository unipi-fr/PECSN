package fair_network;

simple Antenna
{
    parameters:
        @signal[packetQueue](type="double");
        @statistic[packetQueueStat](title="Packet In Queue"; source="packetQueue"; record=vector,stats;);
        
        double timeSlot @unit(ms) = default(1000ms);
        
    gates:
        input packetIn;
        
        input in[];
        output out[];
}
