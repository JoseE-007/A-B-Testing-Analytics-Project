import pandas as pd
import numpy as np
from scipy import stats

# 1. Load and clean the dataset

data = pd.read_csv("randomization.csv").copy()
data = pd.get_dummies(data)


# STEP 1 — Check Current Proportions (Will confirm the imbalance)
print("\nCurrent country proportions by test group:")
print(
    data.groupby("test")[["country_Argentina", "country_Uruguay"]]
        .mean()
)

# STEP 2 — Calculate How Many Extra Rows We Need 
#Counts 
# total users in control and test
n_control = len(data[data["test"] == 0])
n_test = len(data[data["test"] == 1])

# proportion in test group
p_AR_test = data[data["test"] == 1]["country_Argentina"].mean()
p_UR_test = data[data["test"] == 1]["country_Uruguay"].mean()

print("\nTest proportions:")
print("AR:", p_AR_test)
print("UR:", p_UR_test)

#Compute Target Counts for Control 
# how many AR & UR we WANT in control
target_AR_control = int(p_AR_test * n_control)
target_UR_control = int(p_UR_test * n_control)

# current counts in control
current_AR_control = data[(data["test"] == 0) & (data["country_Argentina"] == 1)].shape[0]
current_UR_control = data[(data["test"] == 0) & (data["country_Uruguay"] == 1)].shape[0]

# how many rows to add
rows_needed_AR = target_AR_control - current_AR_control
rows_needed_UR = target_UR_control - current_UR_control

print("\nRows to add:")
print("AR:", rows_needed_AR)
print("UR:", rows_needed_UR) 

# STEP 3 — Oversample From Original Dataset 
# pool of AR and UR users
pool_AR = data[data["country_Argentina"] == 1]
pool_UR = data[data["country_Uruguay"] == 1]

# sample with replacement (important!)
new_AR_rows = pool_AR.sample(rows_needed_AR, replace=True, random_state=42)
new_UR_rows = pool_UR.sample(rows_needed_UR, replace=True, random_state=42)

# change them to control group
new_AR_rows["test"] = 0
new_UR_rows["test"] = 0

# STEP 4 — Append to Dataset
data_adjusted = pd.concat([data, new_AR_rows, new_UR_rows], ignore_index=True)

# STEP 5 — Verify Proportions Are Now Balanced

print("\nNew proportions after correction:")
print(
    data_adjusted.groupby("test")[["country_Argentina", "country_Uruguay"]]
        .mean()
)

# STEP 6 — Run New T-Test

res_adjusted = stats.ttest_ind(
    data_adjusted[data_adjusted["test"] == 1]["conversion"],
    data_adjusted[data_adjusted["test"] == 0]["conversion"],
    equal_var=False
)

print("\nT-test after correction:")
print("T-statistic:", res_adjusted.statistic)
print("P-value:", res_adjusted.pvalue)