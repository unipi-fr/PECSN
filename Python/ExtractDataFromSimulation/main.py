#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode
import omnetDataConverter as odc

import re

def main():
    data = ode.createJsonFromCSV("data/results.csv")
    #ode.saveJsonToFile(data,"debug/data.json")
    dataframes = odc.getArrayDataFrameFromJson(data)
    for dfk in dataframes.keys():
        print("================ "+dfk+" ====================")
        print(dataframes[dfk])
    #dataFrame = odc.createDataFrameFromJson(data)
    #print(dataframe)
    return 0

def examplePlottingDataFromCsv(filename):
    data = pd.read_csv(filename, converters = {
    'attrvalue': ode.parse_if_number,
    'binedges': ode.parse_ndarray,
    'binvalues': ode.parse_ndarray,
    'vectime': ode.parse_ndarray,
    'vecvalue': ode.parse_ndarray})

    vectors = data[data.type=='vector']

    vectors['run'] = vectors['run'].apply(lambda x: x.split("-")[1])
    vectors['module'] = vectors['module'].apply(lambda x: x.split(".")[1])
    vectors = vectors.assign(runmodulename = "run["+vectors.run + "]." + vectors.module)

    #print(vectors.run.unique(),vectors.name.unique(), vectors.module.unique(),vectors.runmodulename.unique())

    somevectors = vectors[vectors.name == 'userThroughputStat:vector'][:]
    for row in somevectors.itertuples():
        plt.plot(row.vectime, row.vecvalue)
    plt.title(somevectors.name.values[0])
    plt.legend(somevectors.runmodulename)
    plt.show()
    return

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