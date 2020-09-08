#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode 
import omnetDataConverter as odc
import test 

import re

def main():
    #test.ExportingDataFromCSVtoDitionaryOfDataFrame("data/results.csv")
    #test.examplePlottingDataFromCsv("data/results.csv")
    test.ExportingCSVToJsonAndThenArrayDataframe(filename="data/results.csv", printFileDebug=True)
    return 0

def saveCsvAsJsonFile(filename):
    df = pd.read_csv (filename + ".csv")
    df.to_json(filename + ".json")

def readFromJson(filename):
    
    #ode.saveJsonToFile(data,"debug/data.json")

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