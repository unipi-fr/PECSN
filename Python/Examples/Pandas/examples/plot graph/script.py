import pandas as pd
import matplotlib.pyplot as plt

print("read data/air_quality_no2.csv...")
air_quality = pd.read_csv("data/air_quality_no2.csv", index_col=0, parse_dates=True)

print(air_quality.head())

air_quality.plot(title ="air_quality.plot()")
air_quality.plot.scatter(title='air_quality.plot.scatter(x=LONDON, y=PARIS)', x="station_london", y="station_paris", alpha=0.5)
air_quality.plot.box(title = 'air_quality.plot.box()')
air_quality.plot.hist(title = 'air_quality.plot.hist()', subplots = True)
plt.show()