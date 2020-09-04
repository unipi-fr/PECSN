#!/usr/bin/python
import sys
import pandas as pd
import matplotlib.pyplot as plt
import json

import re

def findStringBetween(originalStr,str1,str2):
    originalStr
    result = re.search('{str1};(.*){str2}', originalStr)
    return result.group(1)
    
def main():
    readFromJson("data/fixedCQI.json")
    return 0

def transformDictionary(dictionary):
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

    usersColumnNames = []
    
    for i in range(numUser):
        print(i)
        throughputStats = data["users"][i]["userThroughputStat"]["value"]
        userName = "User" + str(i)
        usersColumnNames.append(userName)
        throughputDF[userName] = throughputStats

    throughputDF["Mean"] = throughputDF[usersColumnNames].mean(axis = 1)
    throughputDF["Sum"] = throughputDF[usersColumnNames].sum(axis = 1)

    return throughputDF

def readFromJson(filename):
    dataset = pd.read_json(filename)
    data = transformDictionary(dataset)
    saveDictToJson(data,"data.json")

    dataFrame = getThroughputDataFrame(data)
    print (dataFrame)
    
    #fig, axes = plt.subplots(nrows = 3, ncols = 2, sharex=True)

    axes = dataFrame.plot.line(title='Users values', x="TimeSlots", y="User0", alpha=0.5, style='-o')
    dataFrame.plot.line(title='', x="TimeSlots", y="User1", alpha=0.5, style='-o', ax = axes)
    dataFrame.plot.line(title='', x="TimeSlots", y="User2", alpha=0.5, style='-o', ax = axes)
    dataFrame.plot.line(title='Mean of values for timeslot', x="TimeSlots", y="Mean", alpha=0.5, style='-o')
    dataFrame.plot.line(title='Sum of values for timeslot', x="TimeSlots", y="Sum", alpha=0.5, style='-o')
    
    plt.show()
    return

if __name__== "__main__":
    main()