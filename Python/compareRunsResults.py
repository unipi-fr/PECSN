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
TYPES_OF_RUNS = ["Binomial"]

def main():
    factors = fa.getFactors()

    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
        confidenceIntervals = da.getConfidenceIntervals(jsonProcessed, ["userThroughputTotalStat", "userThroughputStat", "packetDelayStat"])
        groupedUserKeys = extractKeysWithSameUusersNumber(jsonProcessed)
        for userKeys in groupedUserKeys:
            checkFairnessOnEnumeratePlot(jsonProcessed, confidenceIntervals, runFilter = groupedUserKeys[userKeys], statFilter = ["userThroughputTotalStat","packetDelayStat"], numUser = userKeys, confidenceLevel="0.01", graphTitle = userKeys, runMode = resultType, skipVideoPrint = True)
    return

def extractKeysWithSameUusersNumber(jsonProcessed):
    extracted = dict()
    for run in jsonProcessed:
        nuser = run.split(")")[0]+")"
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

def processedJsonToDataFrameFromJSONEnumeratePlot(processedJson, confidenceIntervalsJson, confidenceLevel):
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

                if confidenceLevel is not None:
                    confUp = confDetailStat[userK][confidenceLevel][1]
                    confDown = confDetailStat[userK][confidenceLevel][0]
                    confUpList.append(confUp)
                    confDownList.append(confDown)  

            plotDF[ f"{statK}.X" ] = enumList
            plotDF[ f"{statK}.Y" ] = meanList

            if confidenceLevel is not None:
                plotDF[ f"{statK}.UP" ] = confUpList
                plotDF[ f"{statK}.DOWN" ] = confDownList

        plotDict[runK] = plotDF
            
    return plotDict

def checkFairnessOnEnumeratePlot(processedJson, confidenceIntervalsJson, runFilter, statFilter, numUser = 0, confidenceLevel = "0.01", graphTitle = "", runMode = "", skipVideoPrint = False):
    precessedDataFrame = processedJsonToDataFrameFromJSONEnumeratePlot(processedJson, confidenceIntervalsJson, confidenceLevel)

    colorList = getPlotColors(len(runFilter)) 
    for statK in statFilter:        
        ax = plt.axes(title = graphTitle)
        for i,runK in enumerate(runFilter):
            plotDF = precessedDataFrame[runK]
            Xkey = f"{statK}.X"
            Ykey = f"{statK}.Y" 
            plotDF.plot.scatter(x = Xkey, y = Ykey, ax = ax, c = colorList[i], label = runK)
            if confidenceLevel is not None:
                upKey = f"{statK}.UP"
                downKey = f"{statK}.DOWN"
                plt.fill_between(plotDF[Xkey], plotDF[downKey], plotDF[upKey], color = colorList[i], alpha=.2)

        filename = f"Documentation/images/{runMode}.{statK}.{numUser}"
        plt.savefig(filename + '.svg', format = 'svg', bbox_inches='tight')
        #plt.savefig(filename + '.emp', format = 'emp', bbox_inches='tight')
        if not skipVideoPrint:
            plt.show()
                
    

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

    #filename = "Documentation/fairnessScatterPLot"
    #plt.savefig(filename + '.eps', format = 'eps', bbox_inches='tight')

    plt.show()

def getPlotColors(howMany):
    colormap = cm.viridis
    colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, howMany)]
    return colorlist
    
if __name__ == '__main__':
    main()