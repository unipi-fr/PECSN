#!/usr/bin/python
import configurator as cfg
import os
import json

def main():
    conf = dict()
    conf = cfg.getConfiguration()
    resultsDir = "{projectDir}/simulations/results".format(projectDir = conf["PROJECT_FOLDER"])
    print("Moving into results directory")
    os.chdir(resultsDir)
    print("Moved into => {dir}".format(dir=os.getcwd()))
    print("Extracting results")
    outputPath = conf["OUTPUT_PATH"]
    command = '{path}/bin/scavetool x *.sca *.vec -o {outputPath}/results.csv'.format(path = conf["OMNET_PATH"],outputPath = outputPath)
    print(f"[DEBUG] trying to execute:\n{command}")
    os.system(command)
    print("Results extracted ind => {outputPath}/results.csv".format(outputPath = outputPath))
    return

def loadJsonFromFile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

main()