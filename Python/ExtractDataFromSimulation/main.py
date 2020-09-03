#!/usr/bin/python
import sys
import pandas as pd
import matplotlib.pyplot as plt
import json

def main():
    readFromJson("data/general.json")
    return 0

def transformDictionary(dictionary):
    firstChildKey = next(iter(dictionary))
    vectors = dictionary[firstChildKey]["vectors"]
    numUsers = int(dictionary[firstChildKey]["itervars"]["nUser"])
    data = {"numUsers": numUsers, "users": [dict() for x in range(numUsers)]}

    for i in range(len(vectors)):
        actualVect = vectors[i]
        userID = actualVect["module"]
        intIdUser = int(userID[userID.find("[") + 1])
        aux = actualVect["name"].find(":")
        vectorName = actualVect["name"][0:aux]
        data["users"][intIdUser]["userID"] = intIdUser
        data["users"][intIdUser][vectorName] = {"time": actualVect["time"], "value": actualVect["value"]}
    return data


def saveDictToJson(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def getThroughputMeanValue(dictionary):
    numUser = dictionary["numUsers"]

    meanThroughput = []

    first = True
    for i in range(numUser):
        stats = dictionary["users"][i]
        throughput = stats["userThroughputStat"]

        if first == True:
            meanThroughput = [elem for elem in throughput]
        else:
            meanThroughput = [meanThroughput[i] + throughput[i] for i in range(len(throughput))]

        first = False
        #user[0]

    for i in range(len(meanThroughput)):
        meanThroughput[i] = meanThroughput[i]/numUser

    return meanThroughput

def getThroughputDataFrame(data):
    throughputDF = pd.DataFrame()

    throughputDF["TimeSlots"] = data["users"][0]["userThroughputStat"]["time"]

    numUser = data["numUsers"]

    
    for i in range(numUser):
        throughputStats = data["users"][i]["userThroughputStat"]["value"]
        throughputDF["User" + str(i)] = throughputStats

    throughputDF["Mean"] = throughputDF.mean(axis = 1)

    return throughputDF

def readFromJson(filename):
    dataset = pd.read_json(filename)
    data = transformDictionary(dataset)
    saveDictToJson(data,"data.json")

    dataFrame = getThroughputDataFrame(data)
    print (dataFrame)

    dataFrame.plot.scatter(title='utente[0].plot.scatter(x=timeslots, y=troughput)', x="TimeSlots", y="User0", alpha=0.5)
    dataFrame.plot.line(title='utente[1].plot.scatter(x=timeslots, y=troughput)', x="TimeSlots", y="User1", alpha=0.5, style='-o')
    plt.show()
    return

if __name__== "__main__":
    main()