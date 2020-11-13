import factorialAnalysis as fa
import omnetDataExtractor as ode
import omnetDataConverter as odc
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import math

def main():
    getConfidenceIntervals()

def getConfidenceIntervals(saveToFile = True):
    factors = fa.getFactors()

    jsonConverted = odc.prepareStatisticData(csvFile = "data/resultsGeneral.csv", factors=factors, takeAllRuns = True, levelOfDetail = 1, useJsonFileIfExists = True)
    confidenceIntervalsJSON = constructConfidenceIntervals(jsonConverted, vectorFilter = ["blockPerFrameStat"])

    if saveToFile:
        ode.saveJsonToFile(confidenceIntervalsJSON, "debug/confidenceIntervals.json")

    #plotConfidence(confidenceIntervalsJSON, 'userThroughputTotalStat', "0.01")

    return confidenceIntervalsJSON

def constructConfidenceIntervals(data, vectorFilter = None):
    confidenceIntervals = dict()
    for runk in data.keys():
        run = data[runk]
        runConfidenceIntervals = dict()

        for statk in run.keys():
            runStat = run[statk]
            #print(f"[DEBUG] vectorFilter is not None = {vectorFilter is not None} vect = {vectorFilter}")
            #print(f"[DEBUG] runStat[{statk}] not in vectorFilter = {statk not in vectorFilter}")
            if vectorFilter is not None and statk not in vectorFilter:
                continue

            confidenceIntervalsForStat = constructConfidenceInterval(runStat)

            runConfidenceIntervals[statk] = confidenceIntervalsForStat

        confidenceIntervals[runk] = runConfidenceIntervals

    return confidenceIntervals

def constructConfidenceInterval(data):
    sampleMean = data["mean"]
    n = data["repetitions"]

    values = data["values"]

    sampleVariance = 0
    for value in values:
        sampleVariance += (value - sampleMean)**2
    sampleVariance /= (n-1)

    alphas = [0.1, 0.05, 0.01]

    confidenceInterval = dict()
    for alpha in alphas:
        interval = (math.sqrt(sampleVariance)/math.sqrt(n)) * stats.t.ppf(1- (alpha/2), (n-1))
        lowerBound = sampleMean - interval
        upperBound = sampleMean + interval
        bounds = [lowerBound, upperBound]
        confidenceInterval[str(alpha)] = bounds

    return confidenceInterval

def plotConfidence(data, statToVisualize, confidenceLevel):
    data_dict = {}
    data_dict['RunConf'] = list()
    data_dict['lower'] = list()
    data_dict['upper'] = list()

    for runK in data.keys():
        data_dict['RunConf'].append(runK)
        
        lowerValue = data[runK][statToVisualize][confidenceLevel][0]
        upperValue = data[runK][statToVisualize][confidenceLevel][1]

        data_dict['lower'].append(lowerValue)
        data_dict['upper'].append(upperValue)
        
    dataset = pd.DataFrame(data_dict)

    for lower,upper,y in zip(dataset['lower'],dataset['upper'],range(len(dataset))):
        plt.plot((lower,upper),(y,y),'ro-')
    plt.yticks(range(len(dataset)),list(dataset['RunConf']))

    filename = "Documentation/qqPlot" + statToVisualize
    plt.savefig(filename + '.svg', format = 'svg', bbox_inches='tight')

    plt.show()

if __name__ == '__main__':
    main()