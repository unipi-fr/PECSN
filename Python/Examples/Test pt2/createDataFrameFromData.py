#!/usr/bin/python
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    readFromJson("data/general.json")
    #readFromCSV()
    return 0

def readFromCSV():
    dataset = pd.read_csv("data/general_spread.csv")
    print (df)
    return

def readFromJson(filename):
    dataset = pd.read_json(filename)
    firstChildKey = next(iter(dataset))

    x = dataset[firstChildKey]["vectors"][0]["time"]
    y = dataset[firstChildKey]["vectors"][0]["value"]

    data = {'timeslots':  x, 'delays': y}

    df = pd.DataFrame (data, columns = ['timeslots','delays'])

    print (df)

    df.plot.scatter(title='utente[0].plot.scatter(x=timeslots, y=delays)', x="timeslots", y="delays", alpha=0.5)
    plt.show()
    return

if __name__== "__main__":
    main()