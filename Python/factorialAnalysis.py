import pandas as pd
import itertools as it
import numpy as np
import configurator as cfg
import omnetDataExtractor as ode
from omnetConfIni import OmnetConfIni

def main():

    factors = getFactors(["nUser","userLambda","timeSlot"])

    numFactors = len(factors)
    vectors = [[-1, 1]]*numFactors
    columnNames = [x.name for x in factors]    

    faDataFrame = pd.DataFrame(list(it.product(*vectors)), columns=columnNames)

    combinations = list()
    for i in range(2, numFactors+1):
        combinations = combinations + list(it.combinations(faDataFrame.columns, i))

    for c in combinations:
        print(f"[DEBUG] {c}")
        columnName = '-'.join(c)
        faDataFrame[columnName] = 1
        for otherColumn in c:
            faDataFrame[columnName] = faDataFrame[columnName] * faDataFrame[otherColumn]

    faDataFrame.insert(0, "identity", 1)
        
    #faDataFrame = pd.concat([faDataFrame,(faDataFrame[c[1]].mul(faDataFrame[c[0]]) for c in combinations)], axis=1, keys=combinations)
    #faDataFrame.columns = faDataFrame.columns.map('-'.join)        

    print(faDataFrame)
    return

def getFactors(factors):
    '''
     @file is the ini file where we want to extract factors
     @factors is the list of names of the factors which we want to extract
    '''
    conf = cfg.getConfiguration()
    projectPath = conf["PROJECT_FOLDER"]
    iniFile = f"{projectPath}/simulations/FairNetworkConf.ini"

    iniConf = OmnetConfIni(iniFile)

    return iniConf.getOmnetRunAttr(factors)
    
def factorialAnalysis():
    
    return

main()