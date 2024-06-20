# %%
import pandas as pd
import numpy as np

df = pd.read_csv('proj2_data.csv', sep=';', engine='python', decimal='.')
valid_sep = ';'
valid_dec_sep = False
if len(df.columns) <= 1:
    df = pd.read_csv('proj2_data.csv', sep=',', engine='python', decimal='.')
    valid_sep = ','
if len(df.columns) <= 1:
    df = pd.read_csv('proj2_data.csv', sep='|', engine='python', decimal='.')
    valid_sep = '|'

for i in range(len(df.dtypes)):
    if(df.dtypes.iloc[i] == float):
        valid_dec_sep = True

if not valid_dec_sep:
    df = pd.read_csv('proj2_data.csv', sep = valid_sep, engine='python', decimal=',')

df.to_pickle('proj2_ex01.pkl')
df.head(12)

# %%
file = open("proj2_scale.txt", "r")
data = file.readlines()

for i in range(len(data)):
    data[i] = data[i].strip()

df_copy = df.copy()
cols = []

for column in df_copy.columns:
    if(set(df_copy[column]).issubset(data)):
        cols.append(column)
        for i in range(len(df_copy[column])):
            if df_copy[column][i] in data:
                for j in range(len(data)):
                    if df_copy[column][i] == data[j]:
                        df_copy.loc[i, column] = j+1

df_copy.to_pickle('proj2_ex02.pkl')
df_copy.head()

# %%
df_ex03 = df.copy()

for col in cols:
    df_ex03[col] = pd.Categorical(df_ex03[col], categories=data)

df_ex03.to_pickle('proj2_ex03.pkl')
df_ex03.head()

# %%
import re

cols_for_new_df = []
    
for col in df.columns:
    for i in range(len(df[col])):
        if (str(df[col][i])).isnumeric():
            cols_for_new_df.append(col)

data_for_df = {}
for i in range(len(cols_for_new_df)):
    data_for_df[cols_for_new_df[i]] = df[cols_for_new_df[i]]

ex04_df = pd.DataFrame(data_for_df)

def extract_float(input_string):
    pattern = r"[-+]?\d*\.?\d+"
    match = re.search(pattern, input_string.replace(',', '.'))
    if match:
        return float(match.group())
    else:
        return np.NAN


for col in ex04_df.columns:
    for i in range(len(ex04_df[col])):
        ex04_df.loc[i, col] = extract_float(str(ex04_df.loc[i, col]))

ex04_df.to_pickle('proj2_ex04.pkl')
ex04_df.head(12)

# %%
ex05_cols = []

for col in df.columns:
    if df[col].dtype == 'object' and df[col].str.islower().all() and len(df[col].unique()) <= 10 and col not in cols:
        ex05_cols.append(col)   

d = {}
for i in range(len(ex05_cols)):
    d[i] = pd.get_dummies(df[ex05_cols[i]])
    d[i].to_pickle("proj2_ex05_"+str(i+1)+".pkl")
    print(d[i])

#d[0].head(12)

# %%
d[1].head(12)


