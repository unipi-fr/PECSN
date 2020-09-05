#!/usr/bin/python
import sys
import pandas as pd
import matplotlib.pyplot as plt
import json
    
def main():
    readFromJson("data/3User5Repetition.json")
    return 0

def transformDictionary(dictionary):
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

def getThroughputDataFrames(data):
    throughputDFs = []

    for iteration in data["iterations"]:
        actualDF = getThroughputDataFrame(iteration)
        print(actualDF)
        throughputDFs.append(actualDF)
    
    return throughputDFs

def getThroughputDataFrame(iteration):
    throughputDF = pd.DataFrame()

    #print("[DEBUG]", iteration.keys())
    throughputDF["TimeSlots"] = iteration["users"][0]["userThroughputStat"]["time"]

    usersColumnNames = []
    
    for i,user in enumerate(iteration["users"]):
        throughputStats = user["userThroughputStat"]["value"]
        userName = "User" + str(i)
        usersColumnNames.append(userName)
        throughputDF[userName] = throughputStats

    throughputDF["Mean"] = throughputDF[usersColumnNames].mean(axis = 1)
    throughputDF["Sum"] = throughputDF[usersColumnNames].sum(axis = 1)

    return throughputDF

def readFromJson(filename):
    dataset = pd.read_json(filename)
    data = transformDictionary(dataset)
    print(data)
    saveDictToJson(data, "data.json")

    #dataFrame = getThroughputDataFrames(data)
    
    #print (dataFrame)
    
    #fig, axes = plt.subplots(nrows = 3, ncols = 2, sharex=True)

    #axes = dataFrame.plot.line(title='Users values', x="TimeSlots", y="User0", alpha=0.5, style='-o')
    #dataFrame.plot.line(title='', x="TimeSlots", y="User1", alpha=0.5, style='-o', ax = axes)
    #dataFrame.plot.line(title='', x="TimeSlots", y="User2", alpha=0.5, style='-o', ax = axes)
    #dataFrame.plot.line(title='Mean of values for timeslot', x="TimeSlots", y="Mean", alpha=0.5, style='-o')
    #dataFrame.plot.line(title='Sum of values for timeslot', x="TimeSlots", y="Sum", alpha=0.5, style='-o')
    
    #plt.show()
    return

if __name__== "__main__":
    main()