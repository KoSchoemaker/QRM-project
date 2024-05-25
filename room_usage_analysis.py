import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import os

# See Google Drive Read Me for description of script
# Load the data
file_path = 'TIHM_Dataset/Activity.csv' 
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Extract date part for grouping
data['day'] = data['date'].dt.date

# Calculate the duration spent in each room
data['next_date'] = data.groupby(['patient_id', 'location_name'])['date'].shift(-1)
data['duration'] = (data['next_date'] - data['date']).dt.total_seconds() / 60.0  # Duration in minutes

# Filter out negative durations
data = data[data['duration'] > 0]

# Count the number of visits to each room per day for each patient
room_usage = data.groupby(['patient_id', 'day', 'location_name']).size().reset_index(name='visit_count')

# Function to analyze room usage for a specific patient and room
def analyze_room_usage(room_data):
    # Ensure there's enough data for ADF test
    if len(room_data) > 12:  # Arbitrary threshold, can be adjusted based on requirements
        # Perform the ADF test
        adf_result = adfuller(room_data['visit_count'].dropna())
        
        # Consistency metrics
        std_dev = room_data['visit_count'].std()
        mean_visits = room_data['visit_count'].mean()
        coef_variation = std_dev / mean_visits
        
        return {
            'ADF Statistic': adf_result[0],
            'p-value': adf_result[1],
            'Standard Deviation': std_dev,
            'Coefficient of Variation': coef_variation
        }
    else:
        return {
            'ADF Statistic': None,
            'p-value': None,
            'Standard Deviation': None,
            'Coefficient of Variation': None
        }

# Get the unique patient IDs and room names
patients = room_usage['patient_id'].unique()
rooms = room_usage['location_name'].unique()

# Prepare a list to store the results
results_list = []

# Directory to save plots
plot_dir = 'room_usage_plots'
os.makedirs(plot_dir, exist_ok=True)

# Loop through each patient and each room to perform the analysis
for patient_id in patients:
    for room_name in rooms:
        # Filter data for the specific patient and room
        room_data = room_usage[(room_usage['patient_id'] == patient_id) & 
                               (room_usage['location_name'] == room_name)]
        
        if not room_data.empty:
            # Analyze room usage
            room_results = analyze_room_usage(room_data)
            # Append results to the list
            results_list.append({
                'patient_id': patient_id,
                'location_name': room_name,
                'ADF Statistic': room_results['ADF Statistic'],
                'p-value': room_results['p-value'],
                'Standard Deviation': room_results['Standard Deviation'],
                'Coefficient of Variation': room_results['Coefficient of Variation']
            })
            
            # Plot room usage
            plt.figure(figsize=(10, 6))
            plt.plot(room_data['day'], room_data['visit_count'], marker='o', linestyle='-')
            plt.title(f'Room Usage for {room_name} (Patient {patient_id})')
            plt.xlabel('Date')
            plt.ylabel('Visit Count')
            plt.grid(True)
            # Save the plot as a PNG file
            plot_filename = f'{plot_dir}/room_usage_{patient_id}_{room_name}.png'
            plt.savefig(plot_filename)
            plt.close()

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results_list)

# Save results to a CSV file
results_df.to_csv('room_usage_analysis_results_v1.csv', index=False)

# Display the results
print(results_df.head())

# Aggregate Insights
# Calculate the mean and standard deviation of consistency metrics
agg_results = {
    'mean_std_dev': results_df['Standard Deviation'].mean(),
    'std_std_dev': results_df['Standard Deviation'].std(),
    'mean_coef_var': results_df['Coefficient of Variation'].mean(),
    'std_coef_var': results_df['Coefficient of Variation'].std(),
    'stationary_percentage': results_df[results_df['p-value'] < 0.05].shape[0] / results_df.shape[0] * 100
}

print("Aggregated Results:")
print(agg_results)

# Save aggregated results to a JSON file
import json
with open('aggregated_results.json', 'w') as f:
    json.dump(agg_results, f)

# Analyze absolute time in rooms
threshold = 30  # Time threshold in minutes, used to filter the total duration spent in each room for each patient to ensure that only durations meeting or exceeding the specified threshold are included in the analysis.
time_in_room = data.groupby(['patient_id', 'location_name'])['duration'].sum().reset_index()

# Filter by threshold
time_in_room = time_in_room[time_in_room['duration'] >= threshold]

# Save time in room analysis
time_in_room.to_csv('time_in_room_analysis.csv', index=False)

print(time_in_room.head())
