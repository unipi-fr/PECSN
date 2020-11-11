import omnetDataExtractor as ode
from omnetConfIni import OmnetConfIni

def aggregateJsonOmnetDataOnSameConfigurationRun(dataJson, factors, takeAllRuns = True):
    return convertDataJson(dataJson, factors, takeAllRuns, detailedInformations = True)
 
def convertJsonOmnetDataForFactorialAnalisys(dataJson, factors):
    '''
    trasform a dictionary of Json for omnet data into an new Dictionary with runs aggregated by params

    Note: all values are refeared to mean values
    example:
    {
        "factor1(value1)factor2(value2)...":{
            "vector1": {
                "sumValues": float
                "Values": [float]
                "repetitions": int
                "mean": float
            },
            "vector2": {
                "sumValues": float
                "Values": [float]
                "repetitions": int
                "mean": float
            }
            ...
        },
    }
    '''
    return convertDataJson(dataJson, factors, takeAllRuns = False, detailedInformations = False )


def convertDataJson(dataJson, factors, takeAllRuns = False, detailedInformations = False):
    dataConverted = dict()
    skipped = 0
    total = 0

    for runK in dataJson.keys():
        actualRun = dataJson[runK]
        (result, dictKey) = checkIfRunHasGivenParams(actualRun, factors)
        
        if takeAllRuns or result :
            dataConverted = convertRun(dataConverted, actualRun, dictKey, detailedInformations)
        else:
            skipped += 1
        total += 1
        
    print(f"[INFO] skipped {skipped}/{total} runs")
    return dataConverted


def collectAggregateInformation(vectorSummary, meanAccomulator, meanCount):
    values = ode.checkOrCreateKeyAsValue(vectorSummary, "values", list())
    sumValues = ode.checkOrCreateKeyAsValue(vectorSummary, "sumValues", 0)
    repetition = ode.checkOrCreateKeyAsValue(vectorSummary, "repetitions", 0)

    currentMean = meanAccomulator / meanCount
    values.append(currentMean)
    sumValues += currentMean
    repetition += 1

    vectorSummary["values"] = values
    vectorSummary["sumValues"] = sumValues
    vectorSummary["repetitions"] = repetition
    vectorSummary["mean"] = sumValues / repetition

    return vectorSummary

def extractInformationFromComponent(runSummary, component, numberOfTotalComponents, detailedInformations):
    for vectorK in component.keys():
            vectorSummary = ode.checkOrCreateKeyAsDictionary(runSummary, vectorK)
            
            # those are needed to calculate the mean value of the vector among all users in the current run
            tmpMeanAccomulator = ode.checkOrCreateKeyAsValue(vectorSummary, "tmpMeanAccomulatorValues", 0)
            tmpMeanCount = ode.checkOrCreateKeyAsValue(vectorSummary, "tmpMeanCount", 0)

            currentStats = component[vectorK]["statistics"]
            currentValue = currentStats["mean"]

            tmpMeanAccomulator += currentValue
            tmpMeanCount += 1
            
            # when tmpMeanCount reach the number of components means that all users was visited, so i can calculate aggregate information
            if tmpMeanCount == numberOfTotalComponents:
                vectorSummary = collectAggregateInformation(vectorSummary = vectorSummary, meanAccomulator = tmpMeanAccomulator, meanCount = tmpMeanCount)
                #reset accomulator for next run
                del vectorSummary["tmpMeanCount"]
                del vectorSummary["tmpMeanAccomulatorValues"]
            else:
                vectorSummary["tmpMeanCount"] = tmpMeanCount
                vectorSummary["tmpMeanAccomulatorValues"] = tmpMeanAccomulator
    return runSummary

def convertRun(dataConverted, run, runKeyWithFactors, detailedInformations = False):
    dataConverted = takeAllRunInformations(dataConverted, run, runKeyWithFactors, detailedInformations = detailedInformations)
    return dataConverted

def takeAllRunInformations(dataConverted, run, runKeyWithFactors, detailedInformations):
    runSummary = ode.checkOrCreateKeyAsDictionary(dataConverted, runKeyWithFactors)
    
    # USERS
    nUser = run["nUser"]
    for i in range(nUser):
        userKey = f"user[{i}]"
        actualUser = run[userKey]

        runSummary = extractInformationFromComponent(runSummary, component = actualUser, numberOfTotalComponents = nUser, detailedInformations = detailedInformations)
    # ANTENNA
    runSummary = extractInformationFromComponent(runSummary, component = run["antenna"], numberOfTotalComponents = 1, detailedInformations = detailedInformations)
        
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