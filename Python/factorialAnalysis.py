import pandas as pd
import itertools as it
import numpy as np
import configurator as cfg
import omnetDataExtractor as ode
import omnetDataConverter as odc
import math

from omnetConfIni import OmnetConfIni

def main():
    factorialAnalysis()
    return

def factorialAnalysis():
    factors = getFactors(["nUser","userLambda","timeslot"])
    numberOfFactors = len(factors)
    numberOfExperiments = 2**numberOfFactors

    print(f"[INFO] The number of experiments should be {numberOfExperiments}")

    factorDF = generateDataFrameWithFactors(factors)
    #print(factorDF)
        
    jsonData = ode.createJsonFromCSV(filename = "data/results.csv", skipVectors = True, skipStatistics = False)
    ode.saveJsonToFile(jsonData, "debug/test.json")

    jsonConverted = odc.convertJsonOmnetDataForFactorialAnalisys(jsonData, factors)   
    ode.saveJsonToFile(jsonConverted, "debug/testNew.json")  

    numOfDifferentRuns = len(jsonConverted.keys())    
    if numOfDifferentRuns != numberOfExperiments:
        print(f"[WARNING] The number of different experiments should be {numberOfExperiments} but found {numOfDifferentRuns}")
    else:
        print(f"[INFO] experiments extracted: ({numOfDifferentRuns})")

    vectorName = "userThroughputTotalStat"

    vectorDF, repetitions = appendResultsToDataFrame(factorDF,jsonConverted,factors,vectorName)

    print(vectorDF)

    aggregateDF = calculateAggregateResult(factorDF, vectorDF, vectorName, numberOfExperiments, repetitions)

    #print(aggregateDF)

    joinedDF = joinDataFrames(factorDF, vectorDF, aggregateDF)

    print(joinedDF)

    joinedDF.to_csv("exported.csv", sep = ";")
   
    return

def appendResultsToDataFrame(dataFrame, jsonConverted, factors, vectorName):
    vectorDF = pd.DataFrame()
    numberOfFactors = len(factors)
    numberOfExperiments = 2**numberOfFactors

    dictKeys = list(jsonConverted.keys())
    firstKey = dictKeys[0]

    repetitions = jsonConverted[firstKey][vectorName]["repetitions"]

    vectorDF["identity"] = dataFrame["identity"]

    #inizialize dataframes with NaN
    colunNameList = list()
    columnName = f"{vectorName}"
    colunNameList.append(columnName)
    vectorDF[columnName] = float('NaN')
    for i in range(repetitions):
        columnName = f"{vectorName}[{i}]"
        colunNameList.append(columnName)
        vectorDF[columnName] = float('NaN')
    for i in range(repetitions):
        columnName = f"{vectorName}Error[{i}]"
        colunNameList.append(columnName)
        vectorDF[columnName] = float('NaN')

    vectorDF = vectorDF.drop(["identity"], axis=1)

    for i in range(numberOfExperiments):
        runKey = ""
        for factor in factors:
            factorName = factor.name
            factorIndex = dataFrame.loc[i,factorName]
            factorValue = factor.getMinOrMaxByIndex(factorIndex)
            if(factor.unit == 'ms'):
                factorValue = factorValue/1000
            runKey = runKey+f"{factorName}({factorValue})"
        
        if runKey not in jsonConverted.keys():
            print(f"[WARNING] '{runKey}' skipped because it desn't exists in json")
            continue
            
        vector = jsonConverted[runKey][vectorName]
        values = vector["values"]
        mean = vector["mean"]
        errors = [v - mean for v in values]
        rowList = list()
        rowList.append(mean)
        rowList = rowList + values + errors

        vectorDF.loc[i,colunNameList] = rowList
    return vectorDF, repetitions

def getFactors(factors):
    '''
     @factors is the list of names of the factors which we want to extract form the file in ../PROJECT_FOLDER/simulations/FairNetworkConf.ini
    '''
    conf = cfg.getConfiguration()
    projectPath = conf["PROJECT_FOLDER"]
    iniFile = f"{projectPath}/simulations/FairNetworkConf.ini"

    iniConf = OmnetConfIni(iniFile)

    return iniConf.getOmnetRunAttr(factors)

def generateDataFrameWithFactors(factors):
    numFactors = len(factors)
    vectors = [[-1, 1]]*numFactors
    columnNames = [x.name for x in factors]    

    faDataFrame = pd.DataFrame(list(it.product(*vectors)), columns=columnNames)

    combinations = list()
    for i in range(2, numFactors+1):
        combinations = combinations + list(it.combinations(faDataFrame.columns, i))

    for c in combinations:
        #print(f"[DEBUG] {c}")
        columnName = '-'.join(c)
        faDataFrame[columnName] = 1
        for otherColumn in c:
            faDataFrame[columnName] = faDataFrame[columnName] * faDataFrame[otherColumn]

    faDataFrame.insert(0, "identity", 1)

    return faDataFrame

def calculateAggregateResult(factorDF, vectorDF, vectorName, numberOfExperiments, repetitions):
    aggregateDF = pd.DataFrame()
    
    aggregateDF = aggregateDF.reindex(["Sum", "qi", "SSx", "Variation"])
    
    vectorResults = [ 0 if math.isnan(x) else x for x in vectorDF[vectorName] ]
    #print(vectorResults) 
    sst = 0
    for factorK in factorDF:
        sumValue = sum(factorDF[factorK]*vectorResults)
        meanValue = sumValue / numberOfExperiments
        ssx = float("NaN")
        if factorK != "identity":
            ssx = numberOfExperiments*repetitions*(meanValue**2)
            sst += ssx

        #print(f"{sumValue}, {meanValue}, {ssx}")

        aggregateDF[factorK] = [sumValue, meanValue, ssx, float("NaN")]
    
    sse = 0
    for errork in [x for x in vectorDF.keys() if x.startswith(f"{vectorName}Error")]:
        errorValues = [ 0 if math.isnan(x) else x for x in vectorDF[errork] ]
        sumValue = sum([x*x for x in errorValues])
        sse += sumValue
    aggregateDF[vectorName] = [float("NaN"), float("NaN"), sse, float("NaN")]

    sst += sse

    for aggregateK in aggregateDF:
        if aggregateK == "identity":
            continue
        ssx = aggregateDF.loc["SSx",aggregateK]
        variation = ssx / sst
        aggregateDF.loc["Variation", aggregateK] = variation

    return aggregateDF

def joinDataFrames(factorDF, vectorDF, aggregateDF):
    joinDF = factorDF.copy()
    joinDF = joinDF.join(vectorDF, sort = False)
    joinDF = joinDF.append(aggregateDF, sort = False)

    return joinDF

main()