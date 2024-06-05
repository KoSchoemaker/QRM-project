import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
from datetime import datetime, timedelta

# Load the data
file_path = 'TIHM_Dataset/Activity.csv'  # Update this path to match your file location
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Extract the date and time components
data['date_only'] = data['date'].dt.date
data['time_only'] = data['date'].dt.time

# Convert time to hours since midnight
data['time_hours'] = data['date'].dt.hour + data['date'].dt.minute / 60 + data['date'].dt.second / 3600

# Create a mapping of location names to specific colors
color_map = {
    'Lounge': 'green',
    'Kitchen': 'purple',
    'Bedroom': 'red',
    'Dining Room': 'orange',
    'Bathroom': 'blue'
    # Add other locations and their respective colors here
}

# Get the unique patient ids
patients = data['patient_id'].unique()

# Generate a separate image for each patient
image_paths = []
for patient in patients:
    patient_data = data[data['patient_id'] == patient]

    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot each location with its specific color
    for location, color in color_map.items():
        location_data = patient_data[patient_data['location_name'] == location]
        ax.scatter(location_data['time_hours'], location_data['date_only'], label=location, c=color)

    # Set labels and title
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Date')
    ax.set_title(f'Room Usage Activity Over Time for {patient}')

    # Format x-axis to show time in HH:MM format
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x):02d}:{int((x*60)%60):02d}'))
    ax.xaxis.set_major_locator(plt.MaxNLocator(24))  # Ensure a reasonable number of ticks

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show legend
    ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save the plot as an image
    image_path = f'patient_activity_{patient}.png'
    plt.savefig(image_path)
    image_paths.append(image_path)

    # Close the plot to free memory
    plt.close(fig)

# Print the paths of the generated images
for path in image_paths:
    print(path)
