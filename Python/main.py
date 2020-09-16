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
    #test.ExportingCSVToJsonAndThenArrayDataframe(filename="data/results.csv", printFileDebug=True)
    test.slidingWindowPlots(filename = "data/results.csv", windowSize = 100, minPeriods = 1, center = False)
    #test.dataFrameForEachRunFromCSV("data/results.csv")
    #test.ExportingJsonFromCSV("data/results.csv")
    return 0

if __name__== "__main__":
    main()