# testing
import pandas as pd


df = pd.read_csv('Groceries.csv')
# drop food group category
df1 = df[['Food', 'Price', 'weight (lbs)']]
items = df1.values.tolist()
items2 = df.head(21)
print(items2)
