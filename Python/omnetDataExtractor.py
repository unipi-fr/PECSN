import numpy as np
import pandas as pd
import json
import csv
import sys

def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

def saveJsonToFile(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def loadJsonFromFile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def checkOrCreateKeyAsValue(dictionary, key, value):
    '''
    Returns the object for given @key in the @dictionary, if doesn't exist it creates it as @value
    '''
    if key not in dictionary:
        dictionary[key] = value
    return dictionary[key]

def checkOrCreateKeyAsDictionary(dictionary,key):
    '''
    Returns the object for given @key in the @dictionary, if doesn't exist it creates it as Dictionary
    '''
    if key not in dictionary:
        dictionary[key] = dict()
    return dictionary[key]

def checkOrCreateKeyAsDataFrame(dictionary,key):
    '''
    Returns the object for given @key in the @dictionary, if doesn't exist it creates it as DataFrame
    '''
    if key not in dictionary:
        dictionary[key] = pd.DataFrame()
    return dictionary[key]

def fromMillisecondsToSeconds(value):
    return (float(value[:-2])/1000)

def createJsonFromCSV(filename, skipVectors = False, skipStatistics = False):
    '''
    Converts a OMNET CSV in a more readable json 
    @filename is the path of OMNET CSV file

    an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "simulationTime": double,
            "user[i]":{
                "vectorName": {
                    "statistics": {
                        "count": int,
                        "mean": float,
                        "variance": float,
                        "min": float,
                        "max": float
                        },
                    "time": [],
                    "value": []
                }
            }
        }
    }
    '''
    data = baseElaborateVectorsOfCSV(filename, handlingVectorsFunction = None if skipVectors else handleVectorAsJson, handlingStatisticFunction = None if skipStatistics else handleStatisticsAsJson)             
    return data

def createDataFrameArrayVectorFromCSV(filename):
    '''
    Create an hibrid data structure form an OMNET CSV file
    @filename is the path of OMNET CSV file

    an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "simulationTime": double,
            "vectors":{
                ...
                "rundID.user[i].vectorName": <DataFrame>{
                    "time": [],
                    "rundID.user[i].vectorName": []
                }
                ...
            }
            
            
        }
    }
    '''
    data = baseElaborateVectorsOfCSV(filename,handleVectorAsArraysOfDataFrame)             
    return data

def forEachRunCreateDataFrameFromCSV(filename):
    '''
    Create an hibrid data structure form an OMNET CSV file
    @filename is the path of OMNET CSV file

    an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "simulationTime": double,
            "dataFrame": <DataFrame>{
                # All vector have the same time
                "time": []
                "rundID.user[0].vectorName": [],
                ...
                "rundID.user[i].vectorName": []
            }
        }
    }
    '''
    data = baseElaborateVectorsOfCSV(filename,handleVectorsAsDataFrame)
    return data

def handleVectorAsJson(actualRun,runID,userName,vectorName,timeValues,valueValues, indexList):
    actualUser = checkOrCreateKeyAsDictionary(actualRun,userName)
    actualVector = checkOrCreateKeyAsDictionary(actualUser,vectorName)

    actualVector["time"] = timeValues
    actualVector["value"] = valueValues

    return actualRun

def handleStatisticsAsJson(actualRun,runID,userName,vectorName,statistics):
    actualUser = checkOrCreateKeyAsDictionary(actualRun,userName)
    actualVector = checkOrCreateKeyAsDictionary(actualUser,vectorName)
    
    actualVector["statistics"] = statistics

    return actualRun

def handleVectorAsArraysOfDataFrame(actualRun,runID,userName,vectorName,timeValues, valueValues, indexList):
    vectorID = '{run}.{user}.{vector}'.format(run=runID, user=userName, vector=vectorName) 
    vectors = checkOrCreateKeyAsDictionary(actualRun,"vectors")
    vector = checkOrCreateKeyAsDataFrame(vectors,vectorID)

    vector['time'] = timeValues
    vector[vectorID] = valueValues    
    return actualRun

def handleVectorsAsDataFrame(actualRun, runID, userName, vectorName, timeValues, valueValues, indexList):
    vectorID = '{run}.{user}.{vector}'.format(run=runID, user=userName, vector=vectorName)
    print("Reading '{vector}'".format(vector=vectorID))
    df = checkOrCreateKeyAsValue(actualRun,"DataFrame", pd.DataFrame())
    
    if "time" not in df.keys():
        df['time'] = indexList
        df = df.set_index(['time'])
        df['time'] = indexList

    #print("[DEBUG] df keys: {keys}".format(keys=df.keys()))
    tmpDF = pd.DataFrame()
    tmpDF["time"] = timeValues
    tmpDF[vectorID] = valueValues
    tmpDF = tmpDF.groupby(["time"]).mean()
    tmpDF = tmpDF.reindex(indexList)
    df[vectorID] = tmpDF[vectorID]
    #print("[DEBUG] df keys: {keys}".format(keys=df.keys()))

    actualRun["DataFrame"] = df
    print("vector readed")
    return actualRun

def baseElaborateVectorsOfCSV(filename, handlingVectorsFunction = None, handlingStatisticFunction = None):
    '''
    an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "simulationTime": double,
            "elementCreateByFunction": Object
        }
    }
    '''
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
            
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        data = dict()

        indexList = list()

        for row in reader:
            if 'run' == row[0]:
                continue

            runID = row[0][0:row[0].find("-2020")] # id run ripulito
            actualRun = checkOrCreateKeyAsDictionary(data,runID)
            checkOrCreateKeyAsValue(actualRun,"numberOfFrames",0)
            checkOrCreateKeyAsValue(actualRun,"timeslot",0)
            checkOrCreateKeyAsValue(actualRun,"simulationTime",0)

            if 'itervar' in row and 'simulationTime' in row:
                actualRun['simulationTime'] = float(row[5][:row[5].find("s")])
            if '**.TIMESLOT' in row:
                actualRun['timeslot'] = fromMillisecondsToSeconds(row[5])
            if handlingVectorsFunction is not None and 'vector' in row:
                timeslot = actualRun["timeslot"]
                simulationTime = actualRun["simulationTime"]
                numberOfFrames = int(simulationTime/timeslot)

                if len(indexList) != numberOfFrames:    
                    indexList = [0.0] * numberOfFrames
                    timeSum = timeslot
                    
                    strTimeslot = str(timeslot)
                    timeslotFloatDigits = len(strTimeslot.split(".")[1]) if len(strTimeslot.split(".")) > 1 else 0

                    i = 0
                    while i < numberOfFrames:
                        indexList[i] = timeSum
                        timeSum = round(timeSum + timeslot, timeslotFloatDigits)
                        i+= 1

                    #print(sys.getsizeof(indexList))

                user = row[2].split(".")[1]
                vectorName = row[3].split(":")[0]
                timeValues = [float(x) for x in row[13].split(" ")] 
                valueValues = [float(x) for x in row[14].split(" ")]  

                if vectorName == 'userThroughputStat':
                    actualRun['numberOfFrames']  = len(timeValues)
                
                handlingVectorsFunction(actualRun, runID, user, vectorName, timeValues, valueValues, indexList)
            if handlingStatisticFunction is not None and 'statistic' in row:
                user = row[2].split(".")[1]
                vectorName = row[3].split(":")[0]
                statistics = {
                    "count": int(row[7]),
                    "mean": float(row[9]),
                    "variance": float(row[10]),
                    "min": float(row[11]),
                    "max": float(row[12])
                }

                handlingStatisticFunction(actualRun, runID, user, vectorName, statistics)
    return data