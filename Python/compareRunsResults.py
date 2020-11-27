import omnetDataExtractor as ode
import omnetDataConverter as odc
import factorialAnalysis as fa
import DataAnalysis as da
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np

TYPES_OF_RUNS = ["General","Binomial"]
#TYPES_OF_RUNS = ["General"]

def main():
    fairnessHrizzontalGraphsGroupByUserNumber(printToVideo = False)
    ecdfGraphsGroupByUserNumber(firstQuartile = .025, secondQuartile = .975, printToVideo = False)

def ecdfGraphsGroupByUserNumber(firstQuartile, secondQuartile, printToVideo = False):
    factors = fa.getFactors()

    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
        groupedUserKeys = extractKeysWithSameUusersNumber(jsonProcessed)
        plotDictionary = processedJsonToDataFrameFromJSONEnumeratePlot(jsonProcessed)
        for userKeys in groupedUserKeys:
            pass
            checkFairnessOnEnumeratePlot(plotDictionary, runFilter = groupedUserKeys[userKeys], statFilter = ["userThroughputTotalStat","packetDelayStat"], 
                                        numUser = userKeys,
                                        graphTitle = userKeys, 
                                        runMode = resultType, 
                                        skipVideoPrint = not printToVideo, 
                                        plotECDF = True)
        generateQuantilesTables(plotDictionary, runFilter = jsonProcessed.keys(), statFilter = ["userThroughputTotalStat","packetDelayStat"], 
                                firstQuartile = firstQuartile, 
                                secondQuartile = secondQuartile,  
                                runMode = resultType,
                                printToScreen = True)
    return

def fairnessHrizzontalGraphsGroupByUserNumber(printToVideo = False):
    factors = fa.getFactors()

    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
        groupedUserKeys = extractKeysWithSameUusersNumber(jsonProcessed)
        plotDictionary = processedJsonToDataFrameFromJSONEnumeratePlot(jsonProcessed, confidenceLevel = "0.01", vectorsToBuildConfidenceIntervals = ["userThroughputTotalStat", "userThroughputStat", "packetDelayStat"])
        for userKeys in groupedUserKeys: 
            checkFairnessOnEnumeratePlot(plotDictionary, runFilter = groupedUserKeys[userKeys], statFilter = ["userThroughputTotalStat","packetDelayStat"], 
                                            numUser = userKeys, 
                                            graphTitle = userKeys, 
                                            runMode = resultType, 
                                            skipVideoPrint = not printToVideo)
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

def processedJsonToDataFrameFromJSONEnumeratePlot(processedJson, confidenceLevel = None, vectorsToBuildConfidenceIntervals = []):
    if confidenceLevel is not None:
        confidenceIntervalsJson = da.getConfidenceIntervals(processedJson, vectorsToBuildConfidenceIntervals)
    
    plotDict = dict()

    for runK in processedJson:
        plotDF = pd.DataFrame()
        runStat = processedJson[runK]
        if confidenceLevel is not None:
            confStat = confidenceIntervalsJson[runK]

        for statK in runStat:
            enumList = list()
            meanList = list()
            confUpList = list()
            confDownList = list()

            if "usersRunMeanValues" not in runStat[statK]:
                continue

            usersDetailStat = runStat[statK]["usersRunMeanValues"]
            if confidenceLevel is not None:
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

            (ecdfX, ecdfY) = ecdf(meanList)
            plotDF[ f"{statK}.ecdf.X" ] = ecdfX
            plotDF[ f"{statK}.ecdf.Y" ] = ecdfY

            if confidenceLevel is not None:
                plotDF[ f"{statK}.UP" ] = confUpList
                plotDF[ f"{statK}.DOWN" ] = confDownList

        plotDict[runK] = plotDF
            
    return plotDict

def generateQuantilesTables(plotDicttionary, runFilter, statFilter, firstQuartile = .025, secondQuartile = .975, runMode = "", printToScreen = False, saveToFile = True):
    for statK in statFilter:
        actualDF = pd.DataFrame( columns = [f"Quantile({firstQuartile})", f"Quantile({secondQuartile})", "ratio"])
        for runK in runFilter:
            listOfValues = list() 
            plotDF = plotDicttionary[runK]
            orderedDataK = f"{statK}.ecdf.X"
            actualQuartiles = plotDF[orderedDataK].quantile([firstQuartile, secondQuartile])
            firstQValue = actualQuartiles[firstQuartile]
            secondQValue = actualQuartiles[secondQuartile]
            listOfValues.append(firstQValue)
            listOfValues.append(secondQValue)
            listOfValues.append(firstQValue/secondQValue)
            # add a row with index 'runK'
            actualDF.loc[runK] = listOfValues
        if printToScreen:
            print(f"======= {statK} =======")
            print(actualDF)
        if saveToFile:
            actualDF.to_csv(f"Documentation/{runMode}{statK}quartiles.csv", sep = ";")
    return

def checkFairnessOnEnumeratePlot(plotDicttionary, runFilter, statFilter, numUser = 0, graphTitle = "", runMode = "", skipVideoPrint = False, plotECDF = False):
    colorList = getPlotColors(len(runFilter)) 
    for statK in statFilter:        
        ax = plt.axes(title = graphTitle)
        for i,runK in enumerate(runFilter):
            plotDF = plotDicttionary[runK]
            baseKey = statK
            if plotECDF:
                baseKey = f"{baseKey}.ecdf"
            Xkey = f"{baseKey}.X"
            Ykey = f"{baseKey}.Y" 
            plotDF.plot.scatter(x = Xkey, y = Ykey, ax = ax, c = colorList[i], label = runK)

            upKey = f"{statK}.UP"
            downKey = f"{statK}.DOWN"
            if upKey in plotDF and plotECDF is False: 
                plt.fill_between(plotDF[Xkey], plotDF[downKey], plotDF[upKey], color = colorList[i], alpha=.2)
        ecdf = "ecdf" if plotECDF else ""
        filename = f"Documentation/images/{ecdf}.{runMode}.{statK}.{numUser}"
        plt.savefig(filename + '.svg', format = 'svg', bbox_inches='tight')
        if not skipVideoPrint:
            plt.show()
        else:
            plt.clf()
                
    

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

def ecdf(data):
    """ Compute ECDF """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x,y) 

if __name__ == '__main__':
    main()