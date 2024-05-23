# %% [markdown]
# # Loading Data

# %%
import json

with open('proj5_params.json') as json_file:
    dict1 = json.load(json_file)

# %% [markdown]
# # Exercise 1

# %%
import pandas as pd
import re

df1 = pd.read_csv('proj5_timeseries.csv')
df1.columns = (re.sub(r"[^a-z]", '_', str(x).lower()) for x in df1.columns)

df1[df1.columns[0]] = pd.to_datetime(df1[df1.columns[0]], format='mixed')
df1.set_index(df1.columns[0], inplace=True)

df1 = df1.asfreq(dict1["original_frequency"])

df1.to_pickle('proj5_ex01.pkl')

# %% [markdown]
# # Exercise 2

# %%
df2 = df1.asfreq(dict1["target_frequency"])
df2.to_pickle('proj5_ex02.pkl')

# %% [markdown]
# # Exercise 3

# %%
df3 = df1.copy()
df3 = df3.resample(str(dict1["downsample_periods"])+dict1["downsample_units"]).sum(min_count=dict1['downsample_periods'])
df3.to_pickle('proj5_ex03.pkl')

# %% [markdown]
# # Exercise 4

# %%
df4 = df1.copy()
actual_freq = pd.date_range(start=df4.index[0], end=df4.index[1], freq=df4.index.freq)
new_freq = pd.date_range(start=df4.index[0], end=df4.index[1], freq=str(dict1["upsample_periods"])+dict1["upsample_units"])
scale = (len(new_freq)-1)/(len(actual_freq)-1)
scale
df4 = df4.resample(str(dict1["upsample_periods"])+dict1["upsample_units"]).interpolate(dict1["interpolation"], order=dict1["interpolation_order"])

for col in df4.columns:
    df4[col] = df4[col] / scale

df4.to_pickle('proj5_ex04.pkl')

# %% [markdown]
# # Exercise 5

# %%
df5 = pd.read_pickle('proj5_sensors.pkl')

df5 = df5.pivot(columns='device_id', values='value')

freq = f'{dict1["sensors_periods"]}{dict1["sensors_units"]}'
new_index = pd.date_range(
    start=df5.index.round(freq).min(),
    end=df5.index.round(freq).max(),
    freq=freq
)

df5 = df5.reindex(new_index.union(df5.index)).interpolate()
df5 = df5.reindex(new_index).dropna()

df5.to_pickle('proj5_ex05.pkl')
print(df5)


