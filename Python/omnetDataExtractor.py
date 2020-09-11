import numpy as np
import pandas as pd
import json
import csv


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

def createJsonFromCSV(filename):
    '''
    Converts a OMNET CSV in a more readable json 
    @filename is the path of OMNET CSV file

    an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "user[i]":{
                "vectorName": {
                    "time": [],
                    "value": []
                }
            }
        }
    }
    '''
    #apro e leggo il file 
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        data = dict()   # preparo il dizionario con i dati dei vectors

        for row in reader: # i serve solo a controllare che ci siano effettivamente solo i vector che ci aspettiamo
            if 'run' == row[0]:
                continue

            runID = row[0][0:row[0].find("-2020")] # id run ripulito
            actualRun = checkOrCreateKeyAsDictionary(data,runID)
            checkOrCreateKeyAsValue(actualRun,"numberOfFrames",0)
            checkOrCreateKeyAsValue(actualRun,"timeslot",0)
            
            if '**.TIMESLOT' in row:
                actualRun['timeslot'] = fromMillisecondsToSeconds(row[5])
            if 'vector' in row: # mi interessano solo i vectors
                user = row[2].split(".")[1] # tolgo "FairNetwork."
                vectorName = row[3].split(":")[0] # prendo solo il tipo di vector

                timeValues = [float(x) for x in row[13].split(" ")] # converto una stringa di valori divisa da " " in array di float
                valueValues = [float(x) for x in row[14].split(" ")]

                actualUser = checkOrCreateKeyAsDictionary(actualRun,user) # anche utente e i vector sono dict
                actualVector = checkOrCreateKeyAsDictionary(actualUser,vectorName)

                if vectorName == 'userThroughputStat':
                    actualRun['numberOfFrames']  = len(timeValues)
                
                actualVector["time"] = timeValues # e poi li popolo
                actualVector["value"] = valueValues

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
    data = baseElaborateVectorsOfCSV(filename,dataFrameArrayVector)             
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
    data = baseElaborateVectorsOfCSV(filename,createDataFrameFromVector)
    return data

def dataFrameArrayVector(actualRun,vectorID, timeValues, valueValues):
    vectors = checkOrCreateKeyAsDictionary(actualRun,"vectors")
    vector = checkOrCreateKeyAsDataFrame(vectors,vectorID)

    vector['time'] = timeValues
    vector[vectorID] = valueValues    
    return actualRun

def createDataFrameFromVector(actualRun,vectorID,timeValues, valueValues):

    df = pd.DataFrame()

    timeslot = actualRun['timeslot']
    numberOfFrames = actualRun['numberOfFrames']

    indexList = np.arange(timeslot, numberOfFrames*timeslot + timeslot,timeslot).tolist()
    df['time'] = indexList
    df = df.set_index(['time'])
    df['time'] = indexList

    df = checkOrCreateKeyAsValue(actualRun,"DataFrame", df)

    tmpDF = pd.DataFrame()
    tmpDF["time"] = timeValues
    tmpDF[vectorID] = valueValues
    tmpDF = tmpDF.groupby(["time"]).mean()
    tmpDF = tmpDF.reindex(indexList)
    df[vectorID] = tmpDF[vectorID]

    return actualRun

def baseElaborateVectorsOfCSV(filename,function):
    '''
an example:
    {
        "runID":{
            "numberOfFrame": int,
            "timeslot": double,
            "elementCreateByFunction": Object
        }
    }
    '''
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        data = dict()

        for row in reader:
            if 'run' == row[0]:
                continue

            runID = row[0][0:row[0].find("-2020")] # id run ripulito
            actualRun = checkOrCreateKeyAsDictionary(data,runID)
            checkOrCreateKeyAsValue(actualRun,"numberOfFrames",0)
            checkOrCreateKeyAsValue(actualRun,"timeslot",0)
            
            if '**.TIMESLOT' in row:
                actualRun['timeslot'] = fromMillisecondsToSeconds(row[5])
            if 'vector' in row:
                user = row[2].split(".")[1]
                vectorName = row[3].split(":")[0]
                timeValues = [float(x) for x in row[13].split(" ")] 
                valueValues = [float(x) for x in row[14].split(" ")]
                vectorID = '{run}.{user}.{vector}'.format(run=runID, user=user, vector=vectorName)   

                if vectorName == 'userThroughputStat':
                    actualRun['numberOfFrames']  = len(timeValues)
                
                function(actualRun,vectorID,timeValues,valueValues)
    return data