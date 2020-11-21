import pandas as pd
import DataAnalysis as da
import omnetDataConverter as odc
import factorialAnalysis as fa
import pandas as pd
import numpy as np

STAT_TO_SEE = "blockPerFrameStat"
INTERVAL_OF_VALIDITY_OF_THE_RUN = [15, 24.9]
INTERVAL_OF_CONFIDENCE_USED = "0.1"


blockPerFrameFrameStat = {
    "CONFIDENCE_LEVEL": "0.1",
    "LIST_OF_LOADS":{
        "UNLOADED": [0, 3],
        "NORMAL": [3, 20],
        "HIGH_LOAD": [20, 24.9999999999],
        "SATURATED": [25,25]
    }    
}

conf =  {
    "blockPerFrameStat": blockPerFrameFrameStat,
}
MODES = ["General", "Binomial"]

def main():
    factors = fa.getFactors()
    LIST_OF_STAT = conf.keys()
    jsonConverted = odc.prepareStatisticData(csvFile = "data/resultsGeneral.csv", factors=factors, takeAllRuns = True, levelOfDetail = 4, useJsonFileIfExists = True)
    confidenceIntervals = da.getConfidenceIntervals(jsonConverted, LIST_OF_STAT, saveToFile = True)

    for STAT in LIST_OF_STAT:
        createTable(factors,confidenceIntervals,STAT)
    

def createTable(factors, confidenceIntervals, statName):
    currentStat = conf[statName]
    confidenceLevel = currentStat["CONFIDENCE_LEVEL"]
    listOfLoads = currentStat["LIST_OF_LOADS"]

    if len(factors) > 2:
        raise ValueError(f"More than 2 factors -> {factors} -> abort create table")
    table = inizializeTable(factors[1], factors[0])
    table = populateTable(table, confidenceIntervals, statName , listOfLoads, confidenceLevel)
    print(table)
    

def inizializeTable(factor1, factor2):
    factor1name = factor1.getName()
    factor2name = factor2.getName()

    table = pd.DataFrame()
    table[factor1name] = [f"{factor1name}({x})" for x in factor1.getValues()]
    table = table.set_index(factor1name)
    for value in factor2.getValues():
        table[f'{factor2name}({value})'] = np.nan 
    return table

def populateTable(table, confidenceIntervals, statName ,listOfLoads, confidenceLevel):

    for runK in confidenceIntervals:
        runStatInterval = confidenceIntervals[runK][statName][confidenceLevel]
        meanInterval =( runStatInterval[0] + runStatInterval[1] )/2

        for load in listOfLoads:
            loadInterval = listOfLoads[load]
            
            if meanInterval >= loadInterval[0] and meanInterval <= loadInterval[1]:
                runKeySplitted = [ x+")" for x in runK.split(")")]
                row = runKeySplitted[1]
                column = runKeySplitted[0]
                table.loc[row, column] = load
    return table

def filterRunOLD(data):
    goodRuns = list()

    for runK in data.keys():
        runStatInterval = data[runK][STAT_TO_SEE][INTERVAL_OF_CONFIDENCE_USED]

        if runStatInterval[0] >= INTERVAL_OF_VALIDITY_OF_THE_RUN[0] and runStatInterval[1] <= INTERVAL_OF_VALIDITY_OF_THE_RUN[1]:
            goodRuns.append(runK)

    return goodRuns

def mainOLD():
    factors = fa.getFactors()
    jsonConverted = odc.prepareStatisticData(csvFile = "data/resultsGeneral.csv", factors=factors, takeAllRuns = True, levelOfDetail = 4, useJsonFileIfExists = True)

    data = da.getConfidenceIntervals(jsonConverted, [STAT_TO_SEE], saveToFile = True)
    goodRuns = filterRunOLD(data)

    print("The run in the interaval:", INTERVAL_OF_VALIDITY_OF_THE_RUN, "of the stat", STAT_TO_SEE, "at confidence level:", INTERVAL_OF_CONFIDENCE_USED , "are:")
    #print(goodRuns) brutto !!!

    for run in goodRuns:
        print(run)

if __name__ == '__main__':
    main()
