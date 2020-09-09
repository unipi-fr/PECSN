#!/usr/bin/python
import os
import json

conf = dict()

def main():
    print("loading configuration")
    conf = loadJsonFromFile("configuration.json")
    print("moving into results directory")
    os.chdir(conf["RESULTS_PATH"])
    print("printing directory")
    os.getcwd()
    print("Extracting results")
    os.system('{path}/bin/scavetool x *.sca *.vec -o results.csv'.format(path=conf["OMNET_PATH"]))
    return

def loadJsonFromFile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

main()