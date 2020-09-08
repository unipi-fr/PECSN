#!/usr/bin/python
import os
ANDREA_RESULTS = "C:/Users/andre/Desktop/git/PECSN/Fair-Network/simulations/results"
RESULTS_PATH = ANDREA_RESULTS
ANDREA_OMNET_PATH = "C:/Users/andre/Desktop/omnetpp-5.6.2"
OMNET_PATH = ANDREA_OMNET_PATH

command = 'dir {path}'.format(path=RESULTS_PATH)
print(command)
os.chdir(ANDREA_RESULTS)
os.system("dir")
os.system('{path}/bin/scavetool.exe x *.sca *.vec -o results.csv'.format(path=OMNET_PATH))