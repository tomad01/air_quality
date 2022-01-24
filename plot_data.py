import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('./temp_hum.csv')
cols = data.columns
data[cols[1]] = pd.to_datetime(data[cols[1]])
data = data.set_index(cols[1])
print(len(data))
data[cols[2]][:300].plot()
