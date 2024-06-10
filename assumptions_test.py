import json
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

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

# Check for normality using Shapiro-Wilk test
normality_results = {}
for routine in df['routine'].unique():
    group_data = df[df['routine'] == routine]['sleepEfficiency']
    if len(group_data) >= 3:
        stat, p = stats.shapiro(group_data)
        normality_results[routine] = {'Statistics': stat, 'p-value': p}
        
        # Q-Q plot
        stats.probplot(group_data, dist="norm", plot=plt)
        plt.title(f'Q-Q plot for {routine}')
        plt.savefig(f'qq_plot_{routine}.png')
        plt.close()
    else:
        normality_results[routine] = 'Not enough data points for normality test (less than 3).'

# Check for homogeneity of variances using Levene's test
stat, p = stats.levene(df[df['routine'] == 'routine']['sleepEfficiency'],
                       df[df['routine'] == 'no_routine']['sleepEfficiency'])
homogeneity_results = {'Statistics': stat, 'p-value': p}

# Save results to JSON file
results = {
    "Shapiro-Wilk test for normality": normality_results,
    "Levene's test for homogeneity of variances": homogeneity_results
}

with open('assumption_tests_results_bigger_sample.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Assumption test results saved to assumption_tests_results.json and Q-Q plots saved as PNG files.")
