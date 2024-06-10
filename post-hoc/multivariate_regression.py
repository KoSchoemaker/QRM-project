import json
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the JSON files from the intermediate_results directory
with open('intermediate_results/patient_clustering_results.json', 'r') as f:
    clustering_results = json.load(f)

with open('intermediate_results/efficiencies.json', 'r') as f:
    efficiencies = json.load(f)

with open('intermediate_results/variables.json', 'r') as f:
    variables = json.load(f)

# Convert to DataFrame
df_clustering = pd.DataFrame(list(clustering_results.items()), columns=['patient_id', 'routine'])
df_efficiencies = pd.DataFrame.from_dict(efficiencies, orient='index').reset_index().rename(columns={'index': 'patient_id', 0: 'sleepEfficiency'})
df_variables = pd.DataFrame.from_dict(variables, orient='index').reset_index().rename(columns={'index': 'patient_id'})

# Convert totalSleepTime and totalMinutesInBed from seconds to minutes
df_variables['totalSleepTime'] = df_variables['totalSleepTime'] / 60.0
df_variables['totalMinutesInBed'] = df_variables['totalMinutesInBed'] / 60.0

# Print DataFrames to check for correct loading
print("Clustering Results DataFrame:\n", df_clustering.head())
print("Efficiencies DataFrame:\n", df_efficiencies.head())
print("Variables DataFrame:\n", df_variables.head())

# Merge the DataFrames
df = pd.merge(df_clustering, df_efficiencies, on='patient_id')
df = pd.merge(df, df_variables, on='patient_id')

# Print the columns of the merged DataFrame to check for correct column names
print("Columns in Merged DataFrame:\n", df.columns)

# Map routine values to labels (if necessary)
df['routine'] = df['routine'].map({0: 'routine', 1: 'no_routine'})

# Prepare the data for regression
# Include independent variables such as sleep schedule and room usage
df['sleepSchedule_wake'] = df['sleepSchedule'].apply(lambda x: x['wake'] if isinstance(x, dict) else float('nan'))
df['sleepSchedule_sleep'] = df['sleepSchedule'].apply(lambda x: x['sleep'] if isinstance(x, dict) else float('nan'))
df['roomUsage_Kitchen'] = df['roomUsage'].apply(lambda x: x['Kitchen'] if isinstance(x, dict) else float('nan'))
df['roomUsage_Bedroom'] = df['roomUsage'].apply(lambda x: x['Bedroom'] if isinstance(x, dict) else float('nan'))
df['roomUsage_Bathroom'] = df['roomUsage'].apply(lambda x: x['Bathroom'] if isinstance(x, dict) else float('nan'))
df['roomUsage_Lounge'] = df['roomUsage'].apply(lambda x: x['Lounge'] if isinstance(x, dict) else float('nan'))
df['roomUsage_Hallway'] = df['roomUsage'].apply(lambda x: x['Hallway'] if isinstance(x, dict) else float('nan'))

# Print the DataFrame after adding new columns to verify correctness
print("DataFrame after adding new columns:\n", df.head())

# Print the DataFrame columns to verify the exact name of the sleep efficiency column
print("DataFrame columns:\n", df.columns)

# Verify the correct column names before selection
print("Columns before selection of dependent variables: ", df.columns)

# Define dependent variables
Y = df[['totalSleepTime_x', 'totalMinutesInBed_x']]

# Define independent variables (including intercept)
independent_vars = ['routine', 'sleepSchedule_wake', 'sleepSchedule_sleep', 'roomUsage_Kitchen', 'roomUsage_Bedroom', 'roomUsage_Bathroom', 'roomUsage_Lounge', 'roomUsage_Hallway']
X = df[independent_vars]
X = sm.add_constant(X)

# Ensure all columns are numeric
X = X.apply(pd.to_numeric, errors='coerce')

# Remove rows with any NaN values
X = X.dropna()
Y = Y.dropna()
Y = Y.loc[X.index]


# Print the dependent variables to ensure they are selected correctly
print("Dependent Variables DataFrame:\n", Y.head())
print("IVs Variables DataFrame:\n", X.head())

# Perform Multivariate Regression
model = sm.OLS(Y, X).fit()

# Get the summary of the regression
summary = model.summary()
print(summary)

# Save the regression summary to a text file in the intermediate_results directory
with open('multivariate_regression_summary.txt', 'w') as f:
    f.write(summary.as_text())
