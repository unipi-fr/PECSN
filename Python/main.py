#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode
import test 

import re

def main():
    #test.ExportingDataFromCSVtoDitionaryOfDataFrame("data/results.csv")
    #test.examplePlottingDataFromCsv("data/results.csv")
    #test.ExportingCSVToJsonAndThenArrayDataframe(filename="data/results.csv", printFileDebug=True)
    #test.dataFrameForEachRunFromCSV("data/results.csv")
    #test.ExportingJsonFromCSV("data/results.csv", skipVectors = True, skipStatistics = False)
    test.slidingWindowPlots(filename = "data/results.csv", windowSize = 1, minPeriods = 1, center = False)
    return 0

if __name__== "__main__":
    main()