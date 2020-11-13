import pandas as pd
import DataAnalysis as da
import omnetDataConverter as odc
import factorialAnalysis as fa

STAT_TO_SEE = "blockPerFrameStat"
INTERVAL_OF_VALIDITY_OF_THE_RUN = [0, 25]
INTERVAL_OF_CONFIDENCE_USED = "0.1"

def main():
    factors = fa.getFactors()
    jsonConverted = odc.prepareStatisticData(csvFile = "data/resultsGeneral.csv", factors=factors, takeAllRuns = True, levelOfDetail = 2, useJsonFileIfExists = True)

    data = da.getConfidenceIntervals(jsonConverted, saveToFile = True)
    goodRuns = filterRun(data)

    print("The run in the interaval:", INTERVAL_OF_VALIDITY_OF_THE_RUN, "of the stat", STAT_TO_SEE, "at confidence level:", INTERVAL_OF_CONFIDENCE_USED , "are:")
    #print(goodRuns) brutto !!!

    for run in goodRuns:
        print(run)

def filterRun(data):
    goodRuns = list()

    for runK in data.keys():
        runStatInterval = data[runK][STAT_TO_SEE][INTERVAL_OF_CONFIDENCE_USED]

        if runStatInterval[0] >= INTERVAL_OF_VALIDITY_OF_THE_RUN[0] and runStatInterval[1] <= INTERVAL_OF_VALIDITY_OF_THE_RUN[1]:
            goodRuns.append(runK)

    return goodRuns

if __name__ == '__main__':
    main()
