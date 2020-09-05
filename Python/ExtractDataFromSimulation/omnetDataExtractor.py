import json

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
    firstChildKey = next(iter(dictionary))
    vectors = dictionary[firstChildKey]["vectors"]
    numUsers = int(dictionary[firstChildKey]["itervars"]["nUser"])
    data = {"numUsers": numUsers, "users": [dict() for x in range(numUsers)]}

    for i in range(len(vectors)):
        actualVect = vectors[i]
        userID = actualVect["module"]
        start = userID.find("[")
        finish = userID.find("]")
        intIdUser = int(userID[start + 1 : finish])
        aux = actualVect["name"].find(":")
        vectorName = actualVect["name"][0:aux]
        data["users"][intIdUser]["userID"] = intIdUser
        data["users"][intIdUser][vectorName] = {"time": actualVect["time"], "value": actualVect["value"]}
    return data