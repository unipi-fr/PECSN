#!/usr/bin/python
import configurator as cfg
import os
import json

MODES = ["General", "Binomial"]

def main():
    conf = dict()
    conf = cfg.getConfiguration()
    inputFolder = f"{conf['PROJECT_FOLDER']}/simulations/results"
    outputFolder = conf["OUTPUT_PATH"]
    omnetPath = conf["OMNET_PATH"]

    for mode in MODES:
        extractResult(omnetPath = omnetPath, inputFolder = f"{inputFolder}/{mode}", outputFolder = outputFolder, additionalResultName = mode)
   
    return

def extractResult(omnetPath,inputFolder, outputFolder, skipStatistics = False, skipVector = True , additionalResultName = ""):
    print("Moving into results directory")
    os.chdir(inputFolder)
    print(f"Moved into => {os.getcwd()}")
    print("Extracting results")
    skipString = ("*.sca" if not skipStatistics else "") +" "+ ("*.vec" if not skipVector else "")
    command = f'{omnetPath}/bin/scavetool x {skipString} -o {outputFolder}/results{additionalResultName}.csv -v'
    print(f"[DEBUG] trying to execute:\n{command}")
    os.system(command)
    print(f"Results extracted ind => {outputFolder}/results{additionalResultName}.csv")
    return

def loadJsonFromFile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

main()