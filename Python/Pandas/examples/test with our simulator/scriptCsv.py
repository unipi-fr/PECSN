import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("data/simple_csv.csv", index_col=0, parse_dates=True)
print(dataset.head())
# è uno schifo