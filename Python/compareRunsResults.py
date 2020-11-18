import omnetDataExtractor as ode
import omnetDataConverter as odc
import factorialAnalysis as fa
import DataAnalysis as da
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np

#TYPES_OF_RUNS = ["General","Binomial"]
TYPES_OF_RUNS = ["General"]

def main():
    factors = fa.getFactors()

    #runFilter = ["nUser(25)userLambda(350)", "nUser(50)userLambda(350)", "nUser(100)userLambda(350)", "nUser(150)userLambda(350)", "nUser(200)userLambda(350)"]

    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
        confidenceIntervals = da.getConfidenceIntervals(jsonProcessed, ["userThroughputTotalStat", "userThroughputStat", "packetDelayStat"])
        groupedUserKeys = extractKeysWithSameUusersNumber(jsonProcessed)
        for userKeys in groupedUserKeys:
            checkFairnessOnEnumeratePlot(jsonProcessed, confidenceIntervals, runFilter = groupedUserKeys[userKeys], statFilter = ["userThroughputTotalStat"], numUser = userKeys, plotConfidence = False)

        #checkFairnessOnScatterPlot(confidenceIntervals, runFilter = runFilter, statFilter = ["userThroughputTotalStat"], confidenceLevel="0.01")
        #checkFairnessOnEnumeratePlot(jsonProcessed, confidenceIntervals, runFilter = jsonProcessed, statFilter = ["userThroughputTotalStat"], plotConfidence = True)
    return

def extractKeysWithSameUusersNumber(jsonProcessed):
    extracted = dict()
    for i,run in enumerate(jsonProcessed):
        nuser = run.split(")")[0]+")"
        #print(f"i={i} nuser = '{nuser}'")
        filteredList = ode.checkOrCreateKeyAsValue(extracted, nuser, list())
        filteredList.append(run)
        extracted[nuser] = filteredList
    return extracted
        

def confidenceIntervalsToDataFrameFromJSONScatterPlot(conficenceIntervalsJson, confidenceLevel):
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
    
def checkFairnessOnScatterPlot(confidenceIntervals, runFilter, statFilter, confidenceLevel):
    conficenceIntervalsDataFrame = confidenceIntervalsToDataFrameFromJSONScatterPlot(confidenceIntervals, confidenceLevel)
    
    ax = plt.axes()
    colorList = getPlotColors(len(runFilter))

    for i,runK in enumerate(runFilter):
        confDF = conficenceIntervalsDataFrame[runK]
        for statK in statFilter:
            Xkey = f"{statK}.X"
            Ykey = f"{statK}.Y"
            confDF.plot.scatter(x = Xkey, y = Ykey, ax = ax, c = colorList[i], label = runK)

    plt.xlim((375, 20000)) # default 93000
    plt.ylim((375, 15000)) # default 93000

    filename = "Documentation/fairnessScatterPLot"
    plt.savefig(filename + '.eps', format = 'eps', bbox_inches='tight')

    plt.show()

def processedJsonToDataFrameFromJSONEnumeratePlot(processedJson, confidenceIntervalsJson, plotConfidence):
    plotDict = dict()

    for runK in processedJson:
        plotDF = pd.DataFrame()
        runStat = processedJson[runK]
        confStat = confidenceIntervalsJson[runK]

        for statK in runStat:
            enumList = list()
            meanList = list()
            confUpList = list()
            confDownList = list()

            if "usersRunMeanValues" not in runStat[statK]:
                continue

            usersDetailStat = runStat[statK]["usersRunMeanValues"]
            confDetailStat = confStat[statK]["usersConfidenceIntervals"]

            for i, userK in enumerate(usersDetailStat):
                meanValue = usersDetailStat[userK]["meanOfRepetitions"] 

                enumList.append(i)
                meanList.append(meanValue)

                if plotConfidence:
                    confUp = confDetailStat[userK]["0.01"][1]
                    confDown = confDetailStat[userK]["0.01"][0]
                    confUpList.append(confUp)
                    confDownList.append(confDown)  

            plotDF[ f"{statK}.X" ] = enumList
            plotDF[ f"{statK}.Y" ] = meanList

            if plotConfidence:
                plotDF[ f"{statK}.UP" ] = confUpList
                plotDF[ f"{statK}.DOWN" ] = confDownList

        plotDict[runK] = plotDF
            
    return plotDict

def checkFairnessOnEnumeratePlot(processedJson, confidenceIntervalsJson, runFilter, statFilter, numUser = 0, plotConfidence = False):
    precessedDataFrame = processedJsonToDataFrameFromJSONEnumeratePlot(processedJson, confidenceIntervalsJson, plotConfidence)

    ax = plt.axes()
    colorList = getPlotColors(len(runFilter))

    for i,runK in enumerate(runFilter):
        plotDF = precessedDataFrame[runK]
        for statK in statFilter:
            Xkey = f"{statK}.X"
            Ykey = f"{statK}.Y"

            plotDF.plot.scatter(x = Xkey, y = Ykey, ax = ax, c = colorList[i], label = runK)

            if plotConfidence:
                upKey = f"{statK}.UP"
                downKey = f"{statK}.DOWN"
                plotDF.plot.scatter(x = Xkey, y = upKey, ax = ax, c = colorList[i], label = runK)
                plotDF.plot.scatter(x = Xkey, y = downKey, ax = ax, c = colorList[i], label = runK)

    #plt.xlim((375, 300)) # default 200
    #plt.ylim((375, 15000)) # default 93000

    filename = f"Documentation/fairnessEnumeratePLot{numUser}"
    plt.savefig(filename + '.svg', format = 'svg', bbox_inches='tight')
    
    plt.show()

def getPlotColors(howMany):
    colormap = cm.viridis
    colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, howMany)]
    return colorlist
    
if __name__ == '__main__':
    main()