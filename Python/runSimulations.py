#!/usr/bin/python
import omnetDataExtractor as ode
import os
import json

def main():
    conf = dict()
    print('Loading "configuration.json"')
    conf = ode.loadJsonFromFile("configuration.json")
    print('Moving in simulation directory')
    simulationDir = "{projectFolder}/simulations".format(projectFolder = conf["PROJECT_FOLDER"])
    os.chdir(simulationDir)
    print("Moved into => {dir}".format(dir=os.getcwd()))
    command = '../src/Fair-Network -u Cmdenv -c General -n "../src;." FairNetworkConf.ini -r 0'
    print("[DEBUG] command => {command}".format(command = command))
    os.system(command)
    return

main()