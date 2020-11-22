package fair_network;

simple Antenna
{
    parameters:
        @signal[packetQueue](type="double");
        @statistic[packetQueueStat](title="Packet In Queue"; source="packetQueue"; record=vector,stats;);
        @signal[blockPerFrame](type="int");
        @statistic[blockPerFrameStat](title="Blocks used in current frame"; source="blockPerFrame"; record=vector,stats;);
        @signal[usersSelectingCount](type="int");
        @statistic[usersSelectingCountStat](title="how many times a user is selected"; source="usersSelectingCount"; record=vector,stats;);

        // TO BE REMOVED
        @signal[userPerFrame](type="int");
        @statistic[userPerFrameStat](title="User served in current frame"; source="userPerFrame"; record=vector,stats;);
        @signal[cqiPerFrame](type="double");
        @statistic[cqiPerFrameStat](title="cqi avg in the current frame"; source="cqiPerFrame"; record=vector,stats;);
        
        double timeSlot @unit(ms) = default(1000ms);
        
    gates:
        input packetIn;
        
        input in[];
        output out[];
}
