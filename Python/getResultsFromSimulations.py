#!/usr/bin/python
import os
import json

def main():
    conf = dict()
    print("Loading configuration.json")
    conf = loadJsonFromFile("configuration.json")
    resultsDir = "{projectDir}/simulations/results".format(projectDir = conf["PROJECT_FOLDER"])
    print("Moving into results directory")
    os.chdir(resultsDir)
    print("Moved into => {dir}".format(dir=os.getcwd()))
    print("Extracting results")
    outputPath = conf["OUTPUT_PATH"]
    os.system('{path}/bin/scavetool x *.sca *.vec -o {outputPath}/results.csv'.format(path = conf["OMNET_PATH"],outputPath = outputPath))
    print("Results extracted ind => {outputPath}/results.csv".format(outputPath = outputPath))
    return

def loadJsonFromFile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

main()