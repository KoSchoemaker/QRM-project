import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the data
file_path = 'TIHM_Dataset/Activity.csv' 
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Ensure data is sorted by date for each patient and room
data = data.sort_values(by=['patient_id', 'location_name', 'date'])

# Extract date part for grouping
data['day'] = data['date'].dt.date

# Calculate the duration spent in each room (in minutes)
data['next_date'] = data.groupby(['patient_id', 'location_name'])['date'].shift(-1)
data['duration'] = (data['next_date'] - data['date']).dt.total_seconds() / 60.0  # Duration in minutes

# Filter out negative durations
data = data[data['duration'] > 0]

# Count the number of visits to each room per day for each patient
room_usage = data.groupby(['patient_id', 'day', 'location_name']).size().reset_index(name='visit_count')

# Function to calculate variance of room usage for a specific patient and room
def calculate_variance(room_data):
    # Calculate the variance of visit counts
    variance = room_data['visit_count'].var()
    # Consistency metrics
    std_dev = room_data['visit_count'].std()
    mean_visits = room_data['visit_count'].mean()
    coef_variation = std_dev / mean_visits if mean_visits != 0 else np.nan
    
    return {
        'Variance': variance,
        'Standard Deviation': std_dev,
        'Coefficient of Variation': coef_variation
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
            # Calculate variance and consistency metrics
            variance_results = calculate_variance(room_data)
            # Append results to the list
            results_list.append({
                'patient_id': patient_id,
                'location_name': room_name,
                'Variance': variance_results['Variance'],
                'Standard Deviation': variance_results['Standard Deviation'],
                'Coefficient of Variation': variance_results['Coefficient of Variation']
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
results_df.to_csv('room_usage_variance_results.csv', index=False)

# Display the results
print(results_df.head())

# Aggregate Insights
# Calculate the mean and standard deviation of consistency metrics
agg_results = {
    'mean_variance': results_df['Variance'].mean(),
    'std_variance': results_df['Variance'].std(),
    'mean_std_dev': results_df['Standard Deviation'].mean(),
    'std_std_dev': results_df['Standard Deviation'].std(),
    'mean_coef_var': results_df['Coefficient of Variation'].mean(),
    'std_coef_var': results_df['Coefficient of Variation'].std()
}

print("Aggregated Results:")
print(agg_results)

# Save aggregated results to a JSON file
import json
with open('aggregated_variance_results.json', 'w') as f:
    json.dump(agg_results, f)
