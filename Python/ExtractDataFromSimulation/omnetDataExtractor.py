import numpy as np
import json


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