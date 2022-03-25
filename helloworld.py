# hi
import pandas as pd

# read csv file to pull data
df = pd.read_csv('Groceries.csv')
# drop food group category
df1 = df[['Food', 'Price', 'weight (lbs)']]

items = df1.values.tolist()
newlist = []
print(items)
