package fair_network;

simple User
{
    parameters:
        @signal[packetDelay](type="double");
        @statistic[packetDelayStat](title="Packet delay"; source="packetDelay"; record=vector;);
        @signal[packetBytes](type="int");
        @statistic[packetBytesStat](title="Packet bytes"; source="packetBytes"; record=vector;);
        @signal[userThroughput](type="double");
        @statistic[userThroughputStat](title="User throughput"; source="userThroughput"; record=vector;);
        
        bool useBinomialDistribution = default(false);
    gates:
        input in;
        output out;
        
   	
}
