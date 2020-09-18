import pandas as pd
import numpy as np
import omnetDataExtractor as ode

def main():
    json = ode.createJsonFromCSV(filename = "data/results.csv", skipVectors = True, skipStatistics = False)
    ode.saveJsonToFile(json,"debug/testJson.json")
    return

def factorialAnalysis():
    
    return

main()