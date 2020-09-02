import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_json("data/simple_json.json")
#dataset = eval(open("data/foor_python.json").read())
firstChildKey = next(iter(dataset))

x = dataset[firstChildKey]["vectors"][0]["time"]
y = dataset[firstChildKey]["vectors"][0]["value"]
y2 = y[1:]+y[:1] 

#plt.plot(x, y, "ro") #scatter plot
plt.plot(y, y2, "bo")#lag plot k=1
plt.title("Test Json")
plt.show()
print(x)
print(y)