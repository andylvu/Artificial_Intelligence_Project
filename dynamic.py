import pandas as pd
import numpy as np

# Import csv as dataframe
items = pd.read_csv("groceries.csv")
items = items.drop(columns = ['Category'])
# Note: for the sake of testing the algorithm, price (price) is rounded
items['Price'] = items['Price'].map(lambda x: round(x))

# Convert the df to a 2d array for use by the algorithm
items = items.to_numpy()
items = items.tolist() 

# Grocery total price limit input
limit = 400


'''
Dynamic non-recurisive function to find the optimal knapsack
This uses the top-down method of memoizing items
Stores subproblems in a 2d array for max comparisons
Sacrifices memory usages for vast decrease in computational complexity
Compared to brute force

We want to maximize the return of weight while keeping price <= limit
'''
def dynamic_knapsack(items, limit):
    
    # Generate 2d table for storing subproblems
    # limit determines 0 axis, items determines 1 axis
    table = [[0 for j in range(limit + 1)] for k in range(len(items) + 1)]
 
    result = []
    
    # Iterate over number of items
    for k in range(1, len(items) + 1):
        item, price, weight = items[k-1]
        
        # Iterate over limit as whole numbers
        for j in range(1, limit + 1):
            
            # Do not add if price of item < current limit j
            if price > j:
                table[k][j] = table[k-1][j]
            
            # Add item to table at k,j index if weight is max
            else:
                table[k][j] = max(table[k-1][j], table[k-1][j-price] + weight)
 
    
    # Generate results list finding items in table
    j = limit
    for k in range(len(items), 0, -1):
        was_added = table[k][j] != table[k-1][j]
 
        if was_added:
            item, price, weight = items[k-1]
            result.append(items[k-1])
            j -= price
 
    return result
 
    
# Find total weight & price for items in returned knapsack
def totalvalue(knapsack):
    
    total_price = total_weight = 0
    
    # Sum the total price and weight of items in the knapsack
    for item, price, weight in knapsack:
        total_price  += price
        total_weight += weight
        
    return (total_weight, -total_price) if total_price <= 400 else (0, 0)    


# Driver code
filled_knapsack = dynamic_knapsack(items, limit)
print("Bagged the following items\n  " + '\n  '.join(sorted(item for item,_,_ in filled_knapsack)))
weight, price = totalvalue(filled_knapsack)
print("For a total weight of %i and a total price of %i" % (weight, -price))