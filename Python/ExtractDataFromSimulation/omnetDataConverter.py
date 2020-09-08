import pandas as pd
import numpy as np

def getArrayDataFrameFromJson(data):
    dfs = dict()

    for generalK in data.keys():
        dfs[generalK] = createDataFrameFromJson(data[generalK])

    return dfs

def createDataFrameFromJson(data):
    df = pd.DataFrame()

    numberOfFrames = data['numberOfFrames']
    timeSlot = data['timeslot']
    indexList = np.arange(timeSlot,numberOfFrames + timeSlot,timeSlot).tolist()

    userKeys = filter(lambda x: x.startswith('user['), data.keys())

    df['time'] = indexList
    df = df.set_index(['time'])
    df['time'] = indexList

    for userK in userKeys:
        user = data[userK]
        vetorKeys = user.keys()
        for vectorK in vetorKeys:
            vector = user[vectorK]
            columnValueName = '{user}.{vectorName}'.format(user = userK, vectorName = vectorK)
            tmpDF = pd.DataFrame()
            tmpDF["time"] = vector["time"]
            tmpDF["value"] = vector["value"]
            tmpDF = tmpDF.groupby(["time"]).mean()
            tmpDF = tmpDF.reindex(indexList)

            df[columnValueName] = tmpDF["value"]
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