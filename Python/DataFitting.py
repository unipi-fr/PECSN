import pandas as pd
import matplotlib.pyplot as plt

def main():
    ordStat = list()

    getQQDataFrame([1, 2, 3, 4, 5])

def getNormalq(i):
    normalq = 4.91*((i**(0.14)) - ((1-i)**(0.14)))
    return normalq

def getNormalqs(numValues):
    normalqs = list()

    for i in range(1, numValues):
        normalqs.appen(getNormalq(i - 0.5))

    return normalqs

def getQQDataFrame(ordStat):
    qqDf = pd.DataFrame()
    
    qqDF["normalq"] = getNormalqs(len(ordStat))
    qqDf["ordinatestat"] = ordStat

    return qqDf

main()