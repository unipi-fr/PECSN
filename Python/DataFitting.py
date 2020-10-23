import pandas as pd
import matplotlib.pyplot as plt
import factorialAnalysis as fa 
import seaborn as sns



def main():
    factors = fa.getFactors()

    jsonConverted = fa.prepareData(csvFile = "data/results.csv", factors=factors)

    jsonKeys = list(jsonConverted.keys())
    firstKey = jsonKeys[4]

    statToTest = "userThroughputTotalStat"
    values = jsonConverted[firstKey][statToTest]["values"]

    orderedValues = sorted(values)
    
    print(orderedValues)
    qqDf = getQQDataFrame(range(200))

    sns.lmplot(x='normalq', y='ordinatestat', data=qqDf, fit_reg=True)
    #qqDf.plot()
    plt.show()
    
    plt.savefig(filename + '.svg', bbox_inches='tight')
    plt.savefig(filename + '.png', bbox_inches='tight')

    filename = "Documentation/qqPlot" + statToTest

def getNormalQuantile(i, mean = None, variance = None):
    normalQuantile = 4.91*((i**(0.14)) - ((1-i)**(0.14)))
    if(mean != None and variance == None):
        return (normalQuantile * variance) + mean
    return normalQuantile

def getNormalqs(numValues):
    normalqs = list()

    for i in range(1, numValues+1):
        j = (i - 0.5)/numValues
        print(j)
        normalqs.append(getNormalQuantile(i = j))

    return normalqs

def getQQDataFrame(ordStat):
    qqDf = pd.DataFrame()
    
    qqDf["normalq"] = getNormalqs(len(ordStat))
    qqDf["ordinatestat"] = ordStat

    return qqDf

if __name__ == '__main__':
    main()