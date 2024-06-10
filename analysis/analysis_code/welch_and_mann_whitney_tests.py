import json
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.power as smp

# Load the JSON files
with open('intermediate_results/patient_clustering_results_bigger_sample.json', 'r') as f:
    clustering_results = json.load(f)

with open('intermediate_results/efficiencies.json', 'r') as f:
    efficiencies = json.load(f)

# Convert to DataFrame
df_clustering = pd.DataFrame(list(clustering_results.items()), columns=['patient_id', 'routine'])
df_efficiencies = pd.DataFrame.from_dict(efficiencies, orient='index').reset_index().rename(columns={'index': 'patient_id'})

# Merge the DataFrames
df = pd.merge(df_clustering, df_efficiencies, on='patient_id')

# Map routine values to labels
df['routine'] = df['routine'].map({0: 'routine', 1: 'no_routine'})

# Perform Welch's t-test
routine_efficiency = df[df['routine'] == 'routine']['sleepEfficiency']
no_routine_efficiency = df[df['routine'] == 'no_routine']['sleepEfficiency']

t_stat, p_value_ttest = stats.ttest_ind(routine_efficiency, no_routine_efficiency, equal_var=False)

# Perform the Mann-Whitney U test
u_stat, p_value_mannwhitney = stats.mannwhitneyu(routine_efficiency, no_routine_efficiency, alternative='two-sided')

# Calculate rank-biserial correlation for effect size (Mann-Whitney)
n1 = len(routine_efficiency)
n2 = len(no_routine_efficiency)

def rank_biserial(u_stat, n1, n2):
    rank_biserial = 2 * u_stat / (n1 * n2) - 1
    return rank_biserial

effect_size_mannwhitney = rank_biserial(u_stat, n1, n2)

# Power analysis for Mann-Whitney using TTestIndPower as an approximation
alpha = 0.05  # Significance level
desired_power = 0.80  # Desired power level

power_analysis = smp.TTestIndPower()
power_mannwhitney = power_analysis.solve_power(effect_size=effect_size_mannwhitney, nobs1=n1, alpha=alpha, ratio=n2/n1, alternative='two-sided')

# Calculate required sample size for 80% power
required_n = power_analysis.solve_power(effect_size=effect_size_mannwhitney, power=desired_power, alpha=alpha, ratio=n2/n1, alternative='two-sided')

# Save the results to JSON file
results = {
    "Welch's t-test": {
        "t Statistic": t_stat,
        "p-value": p_value_ttest
    },
    "Mann-Whitney U test": {
        "U Statistic": u_stat,
        "p-value": p_value_mannwhitney,
        "Rank-Biserial Correlation (Effect Size)": effect_size_mannwhitney,
        "Power": power_mannwhitney,
        "Required Sample Size for 80% Power (per group)": required_n
    }
}

with open('test_results_large_sample.json', 'w') as f:
    json.dump(results, f, indent=4)

print(f"Test results saved to test_results_large_sample.json. Welch's t-test: t Statistic: {t_stat}, p-value: {p_value_ttest}. Mann-Whitney U test: U Statistic: {u_stat}, p-value: {p_value_mannwhitney}, Effect Size: {effect_size_mannwhitney}, Power: {power_mannwhitney}, Required Sample Size for 80% Power (per group): {required_n}")
