#!/usr/bin/python
import configurator as cfg
import sys
import os
import json

def main():
    additionalArgs = ' '.join(sys.argv[1:])
    conf = dict()
    conf = cfg.getConfiguration()
    print('Moving in simulation directory')
    simulationDir = "{projectFolder}/simulations".format(projectFolder = conf["PROJECT_FOLDER"])
    os.chdir(simulationDir)
    print("Moved into => {dir}".format(dir=os.getcwd()))
    command = '{projectFolder}/src/Fair-Network -u Cmdenv -c General -n "{projectFolder}/src;{projectFolder}/simulations" FairNetworkConf.ini {additionalArgs}'.format(projectFolder = conf["PROJECT_FOLDER"], additionalArgs = additionalArgs)
    print("[DEBUG] command => {command}".format(command = command))
    os.system(command)
    return

main()