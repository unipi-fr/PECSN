import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

dataset = pd.read_json("data/general.json")
firstChildKey = next(iter(dataset))


x = dataset[firstChildKey]["vectors"][0]["time"]
y = dataset[firstChildKey]["vectors"][0]["value"]
y2 = y[1:]+y[:1] 

Y = y.reshape(-1, 1)
Y2 = y2.reshape(-1, 1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(Y, Y2)  # perform linear regression
Y_pred = linear_regressor.predict(Y)  # make predictions

#plt.plot(x, y, "ro") #scatter plot
plt.scatter(Y, Y2 ) #lag plot k=1
plt.plot(Y, Y_pred, color="red") #lag plot k=1
plt.title("Test Json")
plt.show()
#print(x)
#print(y)