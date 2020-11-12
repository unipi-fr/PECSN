import omnetDataExtractor as ode
from omnetConfIni import OmnetConfIni

def prepareStatisticData(csvFile, factors, takeAllRuns = False, levelOfDetail = 0, activateDebug = False):
    fileName = csvFile.split('/')[-1]
    print("[INFO] creating JSON from csvFile")
    jsonData = ode.createJsonFromCSV(filename = csvFile, skipVectors = True, skipStatistics = False)
    if activateDebug:
        ode.saveJsonToFile(jsonData, f"debug/{fileName}.json")
        print(f"[DEBUG] saved JSON in 'debug/{fileName}.json'")

    activateDebug: print("[INFO] processing JSON for other elaborations")
    jsonConverted = convertDataJson(jsonData, factors, takeAllRuns, levelOfDetail)  
    if activateDebug: 
        ode.saveJsonToFile(jsonConverted, f"debug/{fileName}Processed.json")
        print(f"[DEBUG] saved JSON in 'debug/{fileName}Processed.json'")
    return jsonConverted

def convertDataJson(dataJson, factors, takeAllRuns = False, levelOfDetail = 0):
    dataConverted = dict()
    skipped = 0
    total = 0

    for runK in dataJson.keys():
        actualRun = dataJson[runK]
        (result, dictKey) = checkIfRunHasGivenParams(actualRun, factors)
        
        if takeAllRuns or result :
            dataConverted = convertRun(dataConverted, actualRun, dictKey, levelOfDetail)
        else:
            skipped += 1
        total += 1
        
    print(f"[INFO] skipped {skipped}/{total} runs")
    return dataConverted


def collectAggregateInformation(vectorSummary, tmpVectorSummary, meanAccomulator, meanCount, levelOfDetail):
    # levelOfDetail = 0
    sumValues = ode.checkOrCreateKeyAsValue(tmpVectorSummary, "sumValues", 0)
    repetition = ode.checkOrCreateKeyAsValue(vectorSummary, "repetitions", 0)

    currentMean = meanAccomulator / meanCount
    sumValues += currentMean
    repetition += 1

    if levelOfDetail > 0:
        values = ode.checkOrCreateKeyAsValue(vectorSummary, "values", list())
        values.append(currentMean)
        vectorSummary["values"] = values
    
    tmpVectorSummary["sumValues"] = sumValues
    vectorSummary["repetitions"] = repetition
    vectorSummary["mean"] = sumValues / repetition

    return vectorSummary

def collectDetailedInformation(vectorSummary, tmpVectorSummary , componentKey, meanValue, levelOfDetail):
    # levelOfDetail = 0
    components = componentKey.split('[')[0]+"s"
    componentsRunMeanKey = f"{components}RunMeanValues"

    componentsRunMeanValues = ode.checkOrCreateKeyAsValue(vectorSummary, componentsRunMeanKey, dict())
    actualComponent = ode.checkOrCreateKeyAsValue(componentsRunMeanValues, componentKey, dict())

    tmpCompRunMeanValues = ode.checkOrCreateKeyAsValue(tmpVectorSummary, componentsRunMeanKey, dict())
    actualComponent = ode.checkOrCreateKeyAsValue(componentsRunMeanValues, componentKey, dict())

    tmpActualComponent = ode.checkOrCreateKeyAsValue(tmpCompRunMeanValues, componentKey, dict())
    tmpSumOfValues = ode.checkOrCreateKeyAsValue(tmpActualComponent, "tmpSumOfValues", 0)
    tmpCountOfValues = ode.checkOrCreateKeyAsValue(tmpActualComponent, "tmpCountOfValues", 0)

    tmpSumOfValues += meanValue
    tmpCountOfValues += 1
    if levelOfDetail > 1:
        valueList = ode.checkOrCreateKeyAsValue(actualComponent, "valueList", list())
        valueList.append(meanValue)
        actualComponent["valueList"] = valueList

    tmpActualComponent["tmpSumOfValues"] = tmpSumOfValues
    tmpActualComponent["tmpCountOfValues"] = tmpCountOfValues
    tmpCompRunMeanValues[componentKey] = tmpActualComponent

    actualComponent["meanOfRepetitions"] = tmpSumOfValues / tmpCountOfValues
    componentsRunMeanValues[componentKey] = actualComponent
    vectorSummary[componentsRunMeanKey] = componentsRunMeanValues
    return vectorSummary

def extractInformationFromComponent(runSummary, runTmp, run, componentKey, numberOfTotalComponents, levelOfDetail):
    component = run[componentKey]

    for vectorK in component.keys():
            vectorSummary = ode.checkOrCreateKeyAsDictionary(runSummary, vectorK)
            tmpVectorSum = ode.checkOrCreateKeyAsDictionary(runTmp, vectorK)
            
            # those are needed to calculate the mean value of the vector among all users in the current run
            tmpMeanAccomulator = ode.checkOrCreateKeyAsValue(tmpVectorSum, "tmpMeanAccomulatorValues", 0)
            tmpMeanCount = ode.checkOrCreateKeyAsValue(tmpVectorSum, "tmpMeanCount", 0)

            currentStats = component[vectorK]["statistics"]
            currentValue = currentStats["mean"]

            tmpMeanAccomulator += currentValue
            tmpMeanCount += 1
            vectorSummary = collectDetailedInformation(vectorSummary = vectorSummary, tmpVectorSummary = tmpVectorSum, componentKey = componentKey, meanValue = currentValue, levelOfDetail = levelOfDetail)
            # when tmpMeanCount reach the number of components means that all users was visited, so i can calculate aggregate information
            if tmpMeanCount == numberOfTotalComponents:
                vectorSummary = collectAggregateInformation(vectorSummary = vectorSummary, tmpVectorSummary = tmpVectorSum, meanAccomulator = tmpMeanAccomulator, meanCount = tmpMeanCount, levelOfDetail = levelOfDetail)
                #reset accomulator for next run
                tmpMeanCount = 0
                tmpMeanAccomulator = 0
            
            tmpVectorSum["tmpMeanCount"] = tmpMeanCount
            tmpVectorSum["tmpMeanAccomulatorValues"] = tmpMeanAccomulator
    return runSummary

def convertRun(dataConverted, run, runKeyWithFactors, levelOfDetail):
    dataConverted = takeAllRunInformations(dataConverted, run, runKeyWithFactors, levelOfDetail = levelOfDetail)
    return dataConverted

def takeAllRunInformations(dataConverted, run, runKeyWithFactors, levelOfDetail):
    runSummary = ode.checkOrCreateKeyAsDictionary(dataConverted, runKeyWithFactors)
    tmpDictionary = ode.checkOrCreateKeyAsDictionary(dataConverted, "tmp")
    runTmp = ode.checkOrCreateKeyAsDictionary(tmpDictionary, runKeyWithFactors)
    
    # USERS
    nUser = run["nUser"]
    for i in range(nUser):
        userKey = f"user[{i}]"

        runSummary = extractInformationFromComponent(runSummary, runTmp, run = run, componentKey = userKey, numberOfTotalComponents = nUser, levelOfDetail = levelOfDetail)
    # ANTENNA
    runSummary = extractInformationFromComponent(runSummary, runTmp, run = run, componentKey = "antenna", numberOfTotalComponents = 1, levelOfDetail = levelOfDetail)
        
    return dataConverted

def convertRunOLD(dataConverted, run, runKeyWithFactors):
    runSummary = ode.checkOrCreateKeyAsDictionary(dataConverted, runKeyWithFactors)
    
    nUser = run["nUser"]

    tmpStatDict = dict()
    userVectorNames = list()
    
    for vectorK in run["user[0]"].keys():
        userVectorNames.append(vectorK)
        tmpStatDict[vectorK] = 0

    for i in range(nUser):
        userKey = f"user[{i}]"
        actualUser = run[userKey]

        for vectorK in actualUser.keys():
            currentStats = actualUser[vectorK]["statistics"]
            currentValue = currentStats["mean"]

            tmpStatDict[vectorK] += currentValue

    antenna = run["antenna"]
    
    for vectorK in antenna.keys():
        currentStats = antenna[vectorK]["statistics"]
        currentValue = currentStats["mean"]

        tmpStatDict[vectorK] = currentValue

    for vectorK in tmpStatDict.keys():
        vectorSummary = ode.checkOrCreateKeyAsDictionary(runSummary, vectorK)
        values = ode.checkOrCreateKeyAsValue(vectorSummary, "values", list())
        sumValues = ode.checkOrCreateKeyAsValue(vectorSummary, "sumValues", 0)
        repetition = ode.checkOrCreateKeyAsValue(vectorSummary, "repetitions", 0)

        if vectorK in userVectorNames:
            currentMean = tmpStatDict[vectorK] / nUser
        else:
            currentMean = tmpStatDict[vectorK]
        values.append(currentMean)
        sumValues += currentMean
        repetition += 1

        vectorSummary["values"] = values
        vectorSummary["sumValues"] = sumValues
        vectorSummary["repetitions"] = repetition
        vectorSummary["mean"] = sumValues / repetition

    return dataConverted

def checkIfRunHasGivenParams(run, factors):
    runKeyWithFactors = ""
    result = True
    for factor in factors:
        factorName = factor.name
        factorValue = run[factorName]

        (minV, maxV) = factor.getMinAndMax()
        #print(f"[DEBUG] current factor unit: {factorName}.unit='{factor.unit}' | {factorName}.min='{minV}' | {factorName}.max='{maxV}'")
        if factor.unit == "ms":
            minV = minV / 1000
            maxV = maxV / 1000
        #print(f"[DEBUG] current factor: {factorName}.min='{minV}' | {factorName}.max='{maxV}' - runFactorValue: '{runFactor}'")
        if factorValue != minV and factorValue != maxV:
            result =  False
        runKeyWithFactors = runKeyWithFactors + f"{factorName}({factorValue})"

    return result, runKeyWithFactors