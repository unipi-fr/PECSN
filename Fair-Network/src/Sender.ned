package fair_network;

simple Sender
{
    parameters:
    	double lambda = default(1);
    	int id = default(-1);
    
    gates:
        output out;
}
