import pandas as pd

print("reading data/titanic.csv")
titanic = pd.read_csv("data/titanic.csv")

print(titanic)

print("printing titanic.csv to excel...")
titanic.to_excel('titanic.xlsx', sheet_name='passengers', index=False)
