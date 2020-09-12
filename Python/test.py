import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode
import omnetDataConverter as odc

def ExportingDataFromCSVtoDitionaryOfDataFrame(filename):
    runs = ode.createDataFrameArrayVectorFromCSV(filename)
    for runID in runs.keys():
        vectors = runs[runID]["vectors"]
        vectorName = "packetDelayStat"
        vectorKeys = list(filter(lambda x: x.endswith(vectorName), vectors.keys()))
        fig, axes = plt.subplots(sharex=True)
        for vecID in vectorKeys:
            df = vectors[vecID]
            df.plot.line(title=runID, x="time", y=vecID, alpha=0.5, style='-o', ax = axes)   
    plt.show()
    return

def ExportingCSVToJsonAndThenArrayDataframe(filename, printFileDebug = False):
    data = ode.createJsonFromCSV(filename)
    if printFileDebug:
        ode.saveJsonToFile(data,"debug/data.json")
    dfs = odc.getArrayDataFrameFromJson(data)
    vectorName = "packetDelayStat"

    fig, axes = plt.subplots(sharex=True)

    for i,dfK in enumerate(dfs.keys()):
        df = dfs[dfK]
        vectorKeys = list(filter(lambda x: x.endswith(vectorName), df.keys()))
        df[vectorName+"Mean"] = df[vectorKeys].mean(axis = 1).interpolate(method='linear', limit_direction='forward', axis=0)
        df.plot.line(title=dfK, x="time", y=(vectorName+"Mean"), alpha=0.5, style='-', ax = axes)
        print(df)
    plt.show()
    return

def examplePlottingDataFromCsv(filename):
    data = pd.read_csv(filename, converters = {
    'attrvalue': ode.parse_if_number,
    'binedges': ode.parse_ndarray,
    'binvalues': ode.parse_ndarray,
    'vectime': ode.parse_ndarray,
    'vecvalue': ode.parse_ndarray})

    vectors = data[data.type=='vector']

    vectors.loc[:,('run')] = vectors['run'].apply(lambda x: x.split("-")[1])
    vectors.loc[:,('module')] = vectors['module'].apply(lambda x: x.split(".")[1])
    vectors = vectors.assign(runmodulename = "run["+vectors.run + "]." + vectors.module)

    #print(vectors.run.unique(),vectors.name.unique(), vectors.module.unique(),vectors.runmodulename.unique())

    somevectors = vectors.loc[vectors.name == 'userThroughputStat:vector'][:]
    for row in somevectors.itertuples():
        plt.plot(row.vectime, row.vecvalue)
    plt.title(somevectors.name.values[0])
    plt.legend(somevectors.runmodulename)
    plt.show()
    
    return

def slidingWindowPlots(filename, windowSize, minPeriods, center):
    data = ode.forEachRunCreateDataFrameFromCSV(filename)
    runKeys = data.keys()
    dfSlidingMeans = pd.DataFrame()
    for runK in runKeys:
        actualDF = data[runK]["DataFrame"]
        vectorName = "packetDelayStat"
        vectorKeys = list(filter(lambda x: x.endswith(vectorName), actualDF.keys()))
        tmpDF = actualDF[vectorKeys].rolling(window = windowSize, min_periods = minPeriods, center = center).mean()
        #tmpDF.rename(mapper = lambda colName : '{x}.slidingMean'.format(x = colName), axis = 1)
        dfSlidingMeans = pd.concat([dfSlidingMeans,tmpDF], sort = False, axis=1)
    print(dfSlidingMeans)
    dfSlidingMeans.plot.line(title = "Sliding window mean")
    plt.show()
    return

def dataFrameForEachRunFromCSV(filename):
    data = ode.forEachRunCreateDataFrameFromCSV(filename)
    runKeys = data.keys()
    for runK in runKeys:
        df = data[runK]["DataFrame"]
        #vectorName = "userThroughputStat"
        vectorName = "packetDelayStat"
        vectorKeys = list(filter(lambda x: x.endswith(vectorName), df.keys()))
        print(df[vectorKeys])
    return