import omnetDataExtractor as ode
import omnetDataConverter as odc
import factorialAnalysis as fa

TYPES_OF_RUNS = ["General","Binomial"]

def main():
    factors = fa.getFactors()
    for resultType in TYPES_OF_RUNS:
        csvFile = f"data/results{resultType}.csv"
        jsonProcessed = odc.prepareStatisticData(csvFile,factors, takeAllRuns=True, levelOfDetail=2, useJsonFileIfExists = True, useJsonProcessedIfExists = False)
    return

if __name__ == '__main__':
    main()