package fair_network;

simple SendersHub
{
    parameters:
        @signal[bytesProduced](type="double");
        @statistic[bytesProducedStat](title="Bytes produced"; source="bytesProduced"; record=vector,stats;);

    gates:
        input in[];
        output out;
}
