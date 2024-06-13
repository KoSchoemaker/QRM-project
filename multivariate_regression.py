import json
import pandas as pd
import statsmodels.api as sm

# Load the JSON file
with open('intermediate_results/variables.json', 'r') as f:
    data = json.load(f)

# Convert the JSON data to a DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Convert totalSleepTime and totalMinutesInBed from seconds to minutes
df['totalSleepTime'] = df['totalSleepTime'] / 60.0
df['totalMinutesInBed'] = df['totalMinutesInBed'] / 60.0

# Extract sleep schedule and room usage variables
df['sleepSchedule_wake'] = df['sleepSchedule'].apply(lambda x: x['wake'])
df['sleepSchedule_sleep'] = df['sleepSchedule'].apply(lambda x: x['sleep'])
df['roomUsage_Kitchen'] = df['roomUsage'].apply(lambda x: x['Kitchen'])
df['roomUsage_Bedroom'] = df['roomUsage'].apply(lambda x: x['Bedroom'])
df['roomUsage_Bathroom'] = df['roomUsage'].apply(lambda x: x['Bathroom'])
df['roomUsage_Lounge'] = df['roomUsage'].apply(lambda x: x['Lounge'])
df['roomUsage_Hallway'] = df['roomUsage'].apply(lambda x: x['Hallway'])

# Define independent variables (including intercept)
independent_vars = ['sleepSchedule_wake', 'sleepSchedule_sleep', 'roomUsage_Kitchen', 'roomUsage_Bedroom', 'roomUsage_Bathroom', 'roomUsage_Lounge', 'roomUsage_Hallway']
X = df[independent_vars]
X = sm.add_constant(X)

# Ensure all columns are numeric
X = X.apply(pd.to_numeric, errors='coerce')

# Define and fit the model for totalSleepTime
Y_totalSleepTime = df['totalSleepTime'].apply(pd.to_numeric, errors='coerce').dropna()
X_totalSleepTime = X.loc[Y_totalSleepTime.index]

# Ensure that X and Y are correctly aligned
print("Shapes of X_totalSleepTime and Y_totalSleepTime after dropping NaN values: ", X_totalSleepTime.shape, Y_totalSleepTime.shape)

model_totalSleepTime = sm.OLS(Y_totalSleepTime, X_totalSleepTime).fit()

# Define and fit the model for totalMinutesInBed
Y_totalMinutesInBed = df['totalMinutesInBed'].apply(pd.to_numeric, errors='coerce').dropna()
X_totalMinutesInBed = X.loc[Y_totalMinutesInBed.index]

# Ensure that X and Y are correctly aligned
print("Shapes of X_totalMinutesInBed and Y_totalMinutesInBed after dropping NaN values: ", X_totalMinutesInBed.shape, Y_totalMinutesInBed.shape)

model_totalMinutesInBed = sm.OLS(Y_totalMinutesInBed, X_totalMinutesInBed).fit()

# Get the summaries of the regressions
summary_totalSleepTime = model_totalSleepTime.summary()
summary_totalMinutesInBed = model_totalMinutesInBed.summary()

print(summary_totalSleepTime)
print(summary_totalMinutesInBed)

# Save the regression summaries to text files
with open('post_hoc/multivariate_regression_totalSleepTime_summary.txt', 'w') as f:
    f.write(summary_totalSleepTime.as_text())

with open('post_hoc/multivariate_regression_totalMinutesInBed_summary.txt', 'w') as f:
    f.write(summary_totalMinutesInBed.as_text())
