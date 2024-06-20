# %% [markdown]
# # Introduction

# %%
import pandas as pd
import sqlite3

con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()
result = cur.execute("SELECT count(*) from readings;").fetchall()
df = pd.DataFrame(result)
df

# %%
df = pd.read_sql("SELECT count(*) from readings;", con)
df

# %%
# cur.execute("""
# CREATE INDEX detector_id ON readings (detector_id);
# """).fetchall()
# cur.execute("""
# CREATE INDEX starttime ON readings (starttime);
# """).fetchall()

# %% [markdown]
# # Exercise 1: Basic counting

# %%
df = pd.read_sql("Select Count(distinct(detector_id)) from readings;", con)
df.to_pickle("proj6_ex01_detector_no.pkl")

# %% [markdown]
# # Exercise 2: Some stats for the detectors

# %%
df = pd.read_sql("select distinct(detector_id), count(count), min(starttime), max(starttime) from readings group by detector_id;", con)
df.to_pickle("proj6_ex02_detector_stat.pkl")
df

# %% [markdown]
# # Exercise 3: Moving Window

# %%
df = pd.read_sql("select detector_id, count, LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) AS previous_count from readings where detector_id = 146 limit 500", con)
df.to_pickle('proj6_ex03_detector_146_lag.pkl')
df

# %% [markdown]
# # Exercise 4: Window

# %%
df = pd.read_sql("""
WITH numbered_data AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY starttime) AS row_num
    FROM 
        readings
    WHERE 
        detector_id = 146
)
SELECT 
    detector_id,
    count,
    SUM(count) OVER (
        ORDER BY row_num
        ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING
    ) AS window_sum
FROM 
    numbered_data
LIMIT 500;
""", con)
df.to_pickle('proj6_ex04_detector_146_sum.pkl')
df


