import json
import pandas as pd
import scipy.stats as stats
import numpy as np

# Load the JSON files
with open('intermediate_results/patient_clustering_results.json', 'r') as f:
    clustering_results = json.load(f)

with open('intermediate_results/efficiencies.json', 'r') as f:
    efficiencies = json.load(f)

# Convert to DataFrame
df_clustering = pd.DataFrame(list(clustering_results.items()), columns=['patient_id', 'routine'])
df_efficiencies = pd.DataFrame(list(efficiencies.items()), columns=['patient_id', 'sleep_efficiency'])

# Merge the DataFrames
df = pd.merge(df_clustering, df_efficiencies, on='patient_id')

# Map routine values to labels
df['routine'] = df['routine'].map({0: 'routine', 1: 'no_routine'})

# Perform the Mann-Whitney U test
routine_efficiency = df[df['routine'] == 'routine']['sleep_efficiency']
no_routine_efficiency = df[df['routine'] == 'no_routine']['sleep_efficiency']

u_stat, p_value = stats.mannwhitneyu(routine_efficiency, no_routine_efficiency, alternative='two-sided')

# Calculate rank-biserial correlation for effect size
n1 = len(routine_efficiency)
n2 = len(no_routine_efficiency)

def rank_biserial(u_stat, n1, n2):
    rank_biserial = 2 * u_stat / (n1 * n2) - 1
    return rank_biserial

effect_size = rank_biserial(u_stat, n1, n2)

# Save the results to JSON file
results = {
    "Mann-Whitney U test": {
        "U Statistic": u_stat,
        "p-value": p_value,
        "Rank-Biserial Correlation (Effect Size)": effect_size
    }
}

with open('mann_whitney_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Mann-Whitney U test results saved to mann_whitney_results.json.")
