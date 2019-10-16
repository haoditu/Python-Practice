import pandas as pd
import numpy as np

# visualization
import matplotlib.pyplot as plt

apple = pd.read_csv('appl_1980_2014.csv')

print(apple.head())
print(apple.dtypes)

#Convert Date to datetime
apple['Date'] = pd.to_datetime(apple['Date'])
print(apple['Date'].head())
print(apple.dtypes)

apple = apple.set_index('Date')

# make sure the index is sorted from oldest to newest. 
apple.sort_index(ascending=True)

# Get the last entry on the last day for each month reported #'BM' stands for business month
appleMonth = apple.resample('BM').mean()
print(appleMonth)

#How many days do we have data for?
print((apple.index.max() - apple.index.min()).days)


#Plot the Adj Close Graph
# makes the plot and assign it to a variable
appl_open = apple['Adj Close'].plot(title = "Apple Stock")

# changes the size of the graph
fig = appl_open.get_figure()
fig.set_size_inches(13.5, 9)

plt.show()



