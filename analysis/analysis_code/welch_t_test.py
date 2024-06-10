import json
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower

# Load the JSON files
with open('intermediate_results/patient_clustering_results_bigger_sample.json', 'r') as f:
    clustering_results = json.load(f)

with open('intermediate_results/efficiencies.json', 'r') as f:
    efficiencies = json.load(f)

# Convert to DataFrame
clustering_df = pd.DataFrame(list(clustering_results.items()), columns=['patient_id', 'routine'])
efficiencies_df = pd.DataFrame.from_dict(efficiencies, orient='index').reset_index().rename(columns={'index': 'patient_id', 'sleepEfficiency': 'efficiency'})

# Merge DataFrames on patient_id
df = pd.merge(clustering_df, efficiencies_df, on='patient_id')

# Separate the groups
group_routine = df[df['routine'] == 0]['efficiency']
group_no_routine = df[df['routine'] == 1]['efficiency']

# Perform Welch's t-test
t_stat, p_value = stats.ttest_ind(group_routine, group_no_routine, equal_var=False)

# Calculate Cohen's d
mean_routine = np.mean(group_routine)
mean_no_routine = np.mean(group_no_routine)
std_routine = np.std(group_routine, ddof=1)
std_no_routine = np.std(group_no_routine, ddof=1)
pooled_std = np.sqrt(((std_routine ** 2) + (std_no_routine ** 2)) / 2)
cohens_d = (mean_routine - mean_no_routine) / pooled_std

# Calculate the power of the Welch's t-test
alpha = 0.05  # significance level
effect_size = cohens_d  # using Cohen's d as the effect size
n1 = len(group_routine)
n2 = len(group_no_routine)

# Instantiate the power analysis class
power_analysis = TTestIndPower()
power = power_analysis.solve_power(effect_size=effect_size, nobs1=n1, alpha=alpha, ratio=n2/n1, alternative='two-sided')

# Save the results to a JSON file
results = {
    "t-statistic": t_stat,
    "p-value": p_value,
    "Cohen's d": cohens_d,
    "Power": power
}

with open('welch_test_results.json', 'w') as f:
    json.dump(results, f)

results
