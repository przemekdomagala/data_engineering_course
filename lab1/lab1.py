#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json

df = pd.read_csv('proj1_ex01.csv')

columns_info = []
for column_name in df.columns:
    column_info = {
        'name': column_name,
        'missing': df[column_name].isnull().mean(),
        'type': str(df[column_name].dtype)
    }
    if column_info['type'] == 'float64':
        column_info['type'] = 'float'
    elif column_info['type'] == 'int64':
        column_info['type'] = 'int'
    else:
        column_info['type'] = 'other'
    columns_info.append(column_info)

with open('proj1_ex01_fields.json', 'w') as json_file: #'w' - open for writing, truncating the file first
    json.dump(columns_info, json_file, indent=2)


# In[2]:


columns_info = {}
for column_name in df.columns:
    if df[column_name].dtype == 'O': #'O' - objects
        value_counts = df[column_name].value_counts()
        count = df[column_name].count(),
        unique = df[column_name].nunique(),
        top = value_counts.idxmax()
        freq = df[column_name].value_counts().iloc[0]
        #print(df[column_name].value_counts().nlargest(1))
        columns_info[column_name] = {'count': count[0],
                                    'unique': unique[0],
                                    'top': top,
                                    'freq': freq
                                    }
    else:
        percentiles_summary = df.describe(percentiles=[.25, .5, .75])
        count = df[column_name].count(),
        mean = df[column_name].mean(),
        std = df[column_name].std(),
        min = df[column_name].min(),
        twenty_five = percentiles_summary.loc['25%', column_name],
        fifty = percentiles_summary.loc['50%', column_name],
        seventy_five = percentiles_summary.loc['75%', column_name],
        max = df[column_name].max()
        columns_info[column_name] = {'count': count[0],
                                    'mean': mean[0],
                                    'std': std[0],
                                    'min': min[0],
                                    '25%': twenty_five[0],
                                    '50%': fifty[0],
                                    '75%': seventy_five[0],
                                    'max': max}

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
        
with open('proj1_ex02_stats.json', 'w') as json_file:
    json.dump(columns_info, json_file, cls=NpEncoder, indent=2)
    # json.dump(columns_info, json_file, indent=2, default=str)


# In[3]:


zad3df = df
zad3df.columns = df.columns.str.replace('[^A-Za-z0-9_ ]', '', regex=True)
zad3df.columns = df.columns.str.lower()
zad3df.columns = df.columns.str.replace(' ', '_', regex=False)

zad3df.to_csv('proj1_ex03_columns.csv', index=False)


# In[4]:


import openpyxl

df.to_excel('proj1_ex04_excel.xlsx', index=False)

rows_info = []
for index, row in df.iterrows():
    row_info = {}
    for i in range(len(row)):
        row_info[df.columns[i]] = row.iloc[i]
    rows_info.append(row_info)

with open('proj1_ex04_json.json', 'w') as json_file:
    json.dump(rows_info, json_file, cls=NpEncoder, indent=1)

df.to_pickle('proj1_ex04_pickle.pkl')


# In[5]:


new_df = pd.read_pickle('proj1_ex05.pkl')

selected_columns = new_df.iloc[:, 1:3]
selected_rows = new_df[new_df.index.str.startswith('v')]
result_df = selected_rows.iloc[:, 1:3]
result_df = result_df.fillna('')
result_df
result_df.to_markdown(buf='proj1_ex05_table.md')


# In[6]:


with open('proj1_ex06.json') as f:
    data = json.load(f)
df_3 = pd.json_normalize(data)
df_3.to_pickle('proj1_ex06_pickle.pkl')


# In[ ]:




