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


def convertOmnetJson(filename):
    dictionary = loadJsonFromFile(filename)
    data = convertOmnettDictionary(dictionary)
    return data


def convertOmnettDictionary(dictionary):
    iterator = iter(dictionary.keys())
    lenKeys = len(dictionary.keys())
    data = {"numIterations": lenKeys, "iterations": [dict() for x in range(lenKeys)]}
    iterations = data["iterations"]
    
    for itCounter,childKey in enumerate(iterator):
        vectors = dictionary[childKey]["vectors"]
        numUsers = int(dictionary[childKey]["itervars"]["nUser"])
        actualIteration = {"numUsers": numUsers, "users": [dict() for x in range(numUsers)]}
        iterations[itCounter] = actualIteration
        
        for vec in vectors:
            userID = vec["module"]
            start = userID.find("[")
            finish = userID.find("]")
            intIdUser = int(userID[start + 1 : finish])
            aux = vec["name"].find(":")
            vectorName = vec["name"][0:aux]
            actualIteration["users"][intIdUser]["userID"] = intIdUser
            actualIteration["users"][intIdUser][vectorName] = {"time": vec["time"], "value": vec["value"]}
    return data


def checkOrCreateKeyAsDictionary(dictionary,key):
    if key not in dictionary:
        dictionary[key] = dict()
    return dictionary[key]

def checkOrCreateKeyAsDataFrame(dictionary,key):
    if key not in dictionary:
        dictionary[key] = pd.DataFrame()
    return dictionary[key]


def createJsonFromCSV(filename):
    #apro e leggo il file 
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        data = dict()   # preparo il dizionario con i dati dei vectors

        for row in reader: # i serve solo a controllare che ci siano effettivamente solo i vector che ci aspettiamo
            if 'vector' in row: # mi interessano solo i vectors

                runID = row[0][0:row[0].find("-2020")] # id run ripulito
                user = row[2].split(".")[1] # tolgo "FairNetwork."
                vectorName = row[3].split(":")[0] # prendo solo il tipo di vector
                timeValues = [float(x) for x in row[13].split(" ")] # converto una stringa di valori divisa da " " in array di float
                
                valueValues = [float(x) for x in row[14].split(" ")]
                
                actualRun = checkOrCreateKeyAsDictionary(data,runID) # creo o aggiungo record a dictionary dell'esecuzione i-esima 
                actualUser = checkOrCreateKeyAsDictionary(actualRun,user) # anche utente e i vector sono dict
                actualVector = checkOrCreateKeyAsDictionary(actualUser,vectorName)

                actualVector["time"] = timeValues # e poi li popolo
                actualVector["value"] = valueValues         
    return data


def createDataFrameArrayVectorFromCSV(filename):
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        data = dict()

        for row in reader:
            if 'vector' in row:
                runID = row[0][0:row[0].find("-2020")]
                user = row[2].split(".")[1]
                vectorName = row[3].split(":")[0]
                timeValues = [float(x) for x in row[13].split(" ")] 
                valueValues = [float(x) for x in row[14].split(" ")]

                run = checkOrCreateKeyAsDictionary(data,runID)
                
                vectorID = '{run}.{user}.{vector}'.format(run=runID, user=user, vector=vectorName)
                vector = checkOrCreateKeyAsDataFrame(run,vectorID)

                vector['time'] = timeValues
                vector['value'] = valueValues         
    return data
