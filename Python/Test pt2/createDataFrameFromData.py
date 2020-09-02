import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_json("data/general.json")
firstChildKey = next(iter(dataset))

x = dataset[firstChildKey]["vectors"][0]["time"]
y = dataset[firstChildKey]["vectors"][0]["value"]

data = {'timeslots':  x,
        'delays': y}

df = pd.DataFrame (data, columns = ['timeslots','delays'])

print (df)

df.plot.scatter(title='utente[0].plot.scatter(x=timeslots, y=delays)', x="timeslots", y="delays", alpha=0.5)
plt.show()