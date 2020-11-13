import omnetDataExtractor as ode
import omnetDataConverter as odc
import factorialAnalysis as fa
import DataAnalysis as da
import pandas as pd
import matplotlib.pyplot as plt

TYPES_OF_RUNS = ["General"]#,"Binomial"]

def main():
    factors = fa.getFactors()
    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
        confidenceIntervals = da.getConfidenceIntervals(jsonProcessed)

        confDF = confidenceIntervalsToDataFrameFromJSON(confidenceIntervals, confidenceLevel = "0.01")
        
        checkFairnessOnScatterPlot(confDF, runFilter = ["nUser(100)userLambda(150)"], statFilter= ["userThroughputTotalStat"])
    return

def confidenceIntervalsToDataFrameFromJSON(conficenceIntervalsJson, confidenceLevel):
    confDict = dict()

    lowerBound = 0
    upperBound = 1

    for runK in conficenceIntervalsJson:
        confDF = pd.DataFrame()
        runStat = conficenceIntervalsJson[runK]

        for statK in runStat:
            columnX = list()
            columnY = list()

            if "usersConfidenceIntervals" not in runStat[statK]:
                continue

            usersDetailStat = runStat[statK]["usersConfidenceIntervals"]

            for userK in usersDetailStat:
                confInterval = usersDetailStat[userK][confidenceLevel]

                columnX.append(confInterval[lowerBound])
                columnY.append(confInterval[upperBound])

            confDF[ f"{statK}.X" ] = columnX
            confDF[ f"{statK}.Y" ] = columnY

        confDict[runK] = confDF
            
    return confDict
    
def checkFairnessOnScatterPlot(conficenceIntervalsDataFrame, runFilter, statFilter):
    for runK in runFilter:
        confDF = conficenceIntervalsDataFrame[runK]
        for statK in statFilter:
            Xkey = f"{statK}.X"
            Ykey = f"{statK}.Y"
            confDF.plot.scatter(x = Xkey, y = Ykey, colormap = 'viridis')

    plt.show()

if __name__ == '__main__':
    main()