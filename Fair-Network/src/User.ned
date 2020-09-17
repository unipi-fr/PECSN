package fair_network;

simple User
{
    parameters:
        @signal[packetDelay](type="double");
        @statistic[packetDelayStat](title="Packet delay"; source="packetDelay"; record=vector,stats;);
        @signal[userThroughput](type="double");
        @statistic[userThroughputStat](title="User throughput"; source="userThroughput"; record=vector,stats;);
        @signal[userThroughputTotal](type="double");
        @statistic[userThroughputTotalStat](title="User throughput"; source="userThroughputTotal"; record=stats;);
        
        bool useBinomialDistribution = default(false);
    gates:
        input in;
        output out;
        
   	
}
