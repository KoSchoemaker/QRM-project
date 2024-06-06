import json
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

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

# Initialize results dictionary
results = {}

# Check for normality using Shapiro-Wilk test
for routine in df['routine'].unique():
    stat, p = stats.shapiro(df[df['routine'] == routine]['sleep_efficiency'])
    results[f'Shapiro-Wilk test for {routine}'] = {'Statistics': stat, 'p-value': p}
    
    # Q-Q plot
    stats.probplot(df[df['routine'] == routine]['sleep_efficiency'], dist="norm", plot=plt)
    plt.title(f'Q-Q plot for {routine}')
    plt.savefig(f'qq_plot_{routine}.png')
    plt.close()

# Check for homogeneity of variances using Levene's test
stat, p = stats.levene(df[df['routine'] == 'routine']['sleep_efficiency'],
                       df[df['routine'] == 'no_routine']['sleep_efficiency'])
results['Levene\'s test'] = {'Statistics': stat, 'p-value': p}

# Save results to JSON file
with open('test_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Results saved to test_results.json and Q-Q plots saved as PNG files.")
