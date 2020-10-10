import factorialAnalysis as fa
import omnetDataExtractor as ode
from scipy import stats
import math

def main():
    factors = fa.getFactors()

    jsonConverted = fa.prepareData(csvFile = "data/results.csv", factors=factors)

    confidenceIntervalsJSON = constructConfidenceIntervals(jsonConverted)

    ode.saveJsonToFile(confidenceIntervalsJSON, "debug/confidenceIntervals.json")

def constructConfidenceIntervals(data):
    confidenceIntervals = dict()
    for runk in data.keys():
        run = data[runk]
        runConfidenceIntervals = dict()

        for statk in run.keys():
            runStat = run[statk]

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
        confidenceInterval[alpha] = bounds

    return confidenceInterval


if __name__ == '__main__':
    main()