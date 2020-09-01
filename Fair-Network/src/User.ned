package fair_network;

simple User
{
    parameters:
        @signal[packetDelay](type="double");
        @statistic[packetDelayStat](title="Packet delay"; source="packetDelay"; record=vector,stats;);
        
    gates:
        input in;
        output out;
        
   	
}
