import omnetDataExtractor as ode
from omnetConfIni import OmnetConfIni
    
def convertJsonOmnetDataForFactorialAnalisys(dataJson, factors, takeAllRuns = False):
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
    dataConverted = dict()
    skipped = 0
    total = 0

    for runK in dataJson.keys():
        actualRun = dataJson[runK]
        (result, dictKey) = checkIfRunHasGivenParams(actualRun, factors)
        
        if takeAllRuns or result :
            dataConverted = convertRun(dataConverted, actualRun, dictKey)
        else:
            skipped += 1
        total += 1
        
    print(f"[INFO] skipped {skipped}/{total} runs")

    return dataConverted

def convertRun(dataConverted, run, dictionaryKey):
    runSummary = ode.checkOrCreateKeyAsDictionary(dataConverted, dictionaryKey)
    
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
    dictionaryKey = ""
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
        dictionaryKey = dictionaryKey + f"{factorName}({factorValue})"

    return result, dictionaryKey