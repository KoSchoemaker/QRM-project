import json
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.power as smp

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

# Power analysis using TTestIndPower as an approximation
alpha = 0.05  # Significance level

power_analysis = smp.TTestIndPower()
power = power_analysis.solve_power(effect_size=effect_size, nobs1=n1, alpha=alpha, ratio=n2/n1, alternative='two-sided')

# Save the results to JSON file
results = {
    "Mann-Whitney U test": {
        "U Statistic": u_stat,
        "p-value": p_value,
        "Rank-Biserial Correlation (Effect Size)": effect_size,
        "Power": power
    }
}

with open('mann_whitney_results_with_power.json', 'w') as f:
    json.dump(results, f, indent=4)

print(f'Mann-Whitney U test results with power saved to mann_whitney_results_with_power.json. Power: {power:.4f}')
