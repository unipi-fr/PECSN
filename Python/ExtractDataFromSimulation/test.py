import pandas as pd
import matplotlib.pyplot as plt
import omnetDataExtractor as ode
import omnetDataConverter as odc

def ExportingDataFromCSVtoDitionaryOfDataFrame(filename):
    runs = ode.createDataFrameArrayVectorFromCSV(filename)
    run = runs["General-0"]
    for vecID in run.keys():
        print("================ "+vecID+" ====================")
        print(run[vecID])
    return

def ExportingDataFromCSVtoJson(filename,printFileDebug = False):
    data = ode.createJsonFromCSV(filename)
    if printFileDebug:
        ode.saveJsonToFile(data,"debug/data.json")
    dfs = odc.getArrayDataFrameFromJson(data)
    for dfID in dfs.keys():
        print("================ "+dfID+" ====================")
        print(dfs[dfID])
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