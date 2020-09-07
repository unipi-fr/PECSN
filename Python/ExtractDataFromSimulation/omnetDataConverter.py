import pandas as pd

def getArrayDataFrameFromJson(data):
    dfs = dict()

    for generalK in data.keys():
        dfs[generalK] = createDataFrameFromJson(data[generalK])

    return dfs

def createDataFrameFromJson(data):
    df = pd.DataFrame()
    userKeys = data.keys()
    
    

    for userK in userKeys:
        user = data[userK]
        vetorKeys = user.keys()
        for vectorK in vetorKeys:
            vector = user[vectorK]
            columnTimeName = '{user}.{vectorName}.time'.format(user = userK, vectorName = vectorK)
            columnValueName = '{user}.{vectorName}.value'.format(user = userK, vectorName = vectorK)
            tmpDF = pd.DataFrame()
            tmpDF["time"] = vector["time"]
            tmpDF["value"] = vector["value"]
            tmpDF.groupby("time").mean()
            tmpDF.set_index("time")
            tmpDF.reindex()
            df[columnTimeName] = vector["time"]
            df[columnValueName] = vector["value"]
            
    return df

def getThroughputDataFrames(data):
    throughputDFs = []

    for iteration in iter(data):
        actualDF = getThroughputDataFrame(iteration)
        print(actualDF)
        throughputDFs.append(actualDF)
    
    return throughputDFs

def getThroughputDataFrame(iteration):
    throughputDF = pd.DataFrame()

    #print("[DEBUG]", iteration.keys())
    throughputDF["TimeSlots"] = iteration["users"][0]["userThroughputStat"]["time"]

    usersColumnNames = []
    
    for i,user in enumerate(iteration["users"]):
        throughputStats = user["userThroughputStat"]["value"]
        userName = "User" + str(i)
        usersColumnNames.append(userName)
        throughputDF[userName] = throughputStats

    throughputDF["Mean"] = throughputDF[usersColumnNames].mean(axis = 1)
    throughputDF["Sum"] = throughputDF[usersColumnNames].sum(axis = 1)

    return throughputDF


def getRunPacketDelayAvg(data):
    '''
    partendo da un dictionary (la versione con dataframe) con i dati delle varie run
    calcola la media dei delay di tutti i pacchetti arrivati in ogni timeslot
    @data 
    '''

    
    
    pass