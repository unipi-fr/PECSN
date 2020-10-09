import pandas as pd
import matplotlib.pyplot as plt

def main():
    ordStat = list()

    getQQDataFrame([1, 2, 3, 4, 5])

def getNormalQuantile(i, mean = None, variance = None):
    normalQuantile = 4.91*((i**(0.14)) - ((1-i)**(0.14)))
    if(mean != None and variance == None):
        return (normalQuantile * variance) + mean
    return normalQuantile

def getNormalqs(numValues):
    normalqs = list()

    for i in range(1, numValues):
        normalqs.append(getNormalQuantile(i = i - 0.5))

    return normalqs

def getQQDataFrame(ordStat):
    qqDf = pd.DataFrame()
    
    qqDF["normalq"] = getNormalqs(len(ordStat))
    qqDf["ordinatestat"] = ordStat

    return qqDf

main()