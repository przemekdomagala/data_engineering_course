# %% [markdown]
# ### Task 1

# %%
import pandas as pd

l = []

buffer1 = pd.read_json("proj3_data1.json")
l.append(buffer1)
buffer2 = pd.read_json("proj3_data2.json")
l.append(buffer2)
buffer3 = pd.read_json("proj3_data3.json")
l.append(buffer3)

df = pd.concat([l[0], l[1], l[2]]).reset_index(drop=True)

# %%
import json

json_object = df.to_json(orient='columns')

with open("proj3_ex01_all_data.json", 'w') as my_file:
    json.dump(json.loads(json_object), my_file)

# %% [markdown]
# ### Task 2

# %%
import csv

my_dict = {}
ex02_series = df.isnull().sum()

for index, value in ex02_series.items():
    if(value>0):
        my_dict[index] = value

with open("proj3_ex02_no_nulls.csv", 'w', newline='') as ex02_file:
    writer = csv.writer(ex02_file)
    for key, value in my_dict.items():
        writer.writerow([key, value])

# %% [markdown]
# ### Task 3

# %%
with open("proj3_params.json", 'r') as f:
    ex03dict = json.loads(f.read())

n = len(df)
descr = ['']*n
counter = 1

for col in ex03dict["concat_columns"]:
    for i in range(n):
        str_ = descr[i]
        str_ += df[col].iloc[i]
        if(counter<len(ex03dict["concat_columns"])):
            str_ += " "
        descr[i] = str_
    counter += 1

ex03df = df.assign(description=descr)
ex03_json = ex03df.to_json(orient='columns')

with open("proj3_ex03_descriptions.json", 'w') as ex03_file:
    json.dump(json.loads(ex03_json), ex03_file)

# %% [markdown]
# ### Task 4

# %%
ex04df = pd.read_json("proj3_more_data.json")

merged_df = pd.merge(ex03df, ex04df, on=ex03dict["join_column"], how="left")
ex04_json = merged_df.to_json(orient='columns')

with open("proj3_ex04_joined.json", 'w') as ex04_file:
    json.dump(json.loads(ex04_json), ex04_file)

# %% [markdown]
# ### Task 5
# 

# %% [markdown]
# #### A)

# %%
for i, r in merged_df.iterrows():
    description = r['description']
    r.drop('description').to_json('proj3_ex05_' + description.lower().replace(' ', '_') + '.json')

# %% [markdown]
# #### B)

# %%
df_5 = merged_df.copy()
for col in df_5.columns:
    if col in ex03dict['int_columns']:
        df_5[col] = df_5[col].where(df_5[col].notna(), -1).astype('int')
        df_5[col] = df_5[col].astype('object')
        df_5[col] = df_5[col].where(df_5[col] != -1, None)

for i, r in df_5.iterrows():
    description = r['description']
    r.drop('description').to_json('proj3_ex05_int_' + description.lower().replace(' ', '_') + '.json')

# %% [markdown]
# ### Task 6

# %%
from statistics import mean

vals = {}

for pair in ex03dict["aggregations"]:
    if pair[1] == 'min':
        vals["min_"+pair[0]] = merged_df[pair[0]].min()
    elif pair[1] == 'max':
        vals["max_"+pair[0]] = merged_df[pair[0]].max()
    elif pair[1] == 'mean':
        vals["mean_"+pair[0]] = merged_df[pair[0]].mean()
    elif pair[1] == 'mean':
        vals["count_"+pair[0]] = merged_df[pair[0]].count()
    elif pair[1] == 'mean':
        vals["median_"+pair[0]] = merged_df[pair[0]].median()
    elif pair[1] == 'mean':
        vals["mode_"+pair[0]] = merged_df[pair[0]].mode()
    elif pair[1] == 'mean':
        vals["std_"+pair[0]] = merged_df[pair[0]].std()
    elif pair[1] == 'mean':
        vals["var_"+pair[0]] = merged_df[pair[0]].var()

my_json = json.dumps(vals)
with open("proj3_ex06_aggregations.json", 'w') as _file_:
    json.dump(json.loads(my_json), _file_)

# %% [markdown]
# ### Task 7

# %%
groups = merged_df.groupby(ex03dict['grouping_column']).filter(lambda x: len(x) > 1)

df_7 = pd.DataFrame()
for i,g in groups.groupby(ex03dict['grouping_column']):
       df_7[i] = g.mean(numeric_only=True)

df_7 = df_7.T
df_7.index.name = ex03dict['grouping_column']
df_7.to_csv('proj3_ex07_groups.csv', header=True, index=True)
df_7

# %% [markdown]
# ### Task 8

# %% [markdown]
# #### A)

# %%
df8_1 = merged_df.pivot_table(index=ex03dict["pivot_index"], columns=ex03dict["pivot_columns"], values=ex03dict["pivot_values"], aggfunc='max')
df8_1.to_pickle("proj3_ex08_pivot.pkl")
df8_1

# %% [markdown]
# #### B)

# %%
df8_2 = pd.melt(merged_df, id_vars=ex03dict["id_vars"])
df8_2.to_csv("proj3_ex08_melt.csv", index=False)
df8_2

# %% [markdown]
# #### C)

# %%
df = pd.read_csv('proj3_statistics.csv')
df.columns
l = []
for x in df.columns:
    x = x.split("_")
    if x[0] in merged_df[ex03dict["pivot_index"]].values:
        l.append(x[0])

df = pd.wide_to_long(df, stubnames=set(l), i='Country', j="Year", sep="_")
df.to_pickle('proj3_ex08_stats.pkl')
df.head(16)


