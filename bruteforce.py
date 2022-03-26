from itertools import combinations
import pandas as pd
import time

# read csv file to pull data
df = pd.read_csv('Groceries.csv')
# drop food group category
df1 = df[['Food', 'Price', 'weight (lbs)']]


# makes all possible combinations
def anycomb(items):
    'return combinations of any length from the items '
    return (comb for r in range(1, len(items) + 1)for comb in combinations(items, r))


# gets total value of the combination
def totalvalue(comb):
    'Totalise a particular combination of items'
    total_price = total_weight = 0
    for item, price, weight in comb:
        total_price += price
        total_weight += weight
    return (total_weight, -total_price) if total_price <= 100 else (0, 0)


items = df1.values.tolist()
# k = size of list desired
k = 15
n = len(items)
for i in range(0, n - k):
    items.pop()


# start time
start_time = time.time()
# max weight or min price if values equal
bagged = max(anycomb(items), key=totalvalue)
print("Bagged the following items\n  " + '\n  '.join(sorted(item for item, _, _ in bagged)))
weight, price = totalvalue(bagged)
print("for a total weight of %i and a total price of %i" % (weight, -price))
print("--- %s seconds ---" % (time.time() - start_time))
