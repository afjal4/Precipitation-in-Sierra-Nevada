import numpy
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller

#"-119.9 , 37.4",
df = pd.read_csv('data/precipitation/Datapoint1.csv')
df['year'] = range(1924, 1924 + len(df))
df['year'] = pd.to_datetime(df['year'], format='%Y')
df.set_index('year', inplace=True)

plt.plot(df.index, df['ppt'])
plt.show()
