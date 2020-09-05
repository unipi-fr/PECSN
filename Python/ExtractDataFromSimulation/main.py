#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode

import re

def saveCsvAsJsonFile(filename):
    df = pd.read_csv (filename + ".csv")
    df.to_json(filename + ".json")
    
def main():
    readFromJson("data/fixedCQI.json")
    #saveCsvAsJsonFile("data/prova")
    return 0

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
    data = ode.convertOmnetJson(filename)
    ode.saveJsonToFile(data,"debug/data.json")

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