import pandas as pd
import numpy as np
from statsmodels.stats.power import TTestIndPower
import matplotlib.pyplot as plt

# Load the variance results
file_path = 'TIHM_Dataset/Activity.csv'  # Update with your actual file path
results_df = pd.read_csv(file_path)

# Display the results
print(results_df.head())

# Calculate statistical power
# Define parameters for power analysis
effect_size = 0.5  # This is an example, determine based on your context
alpha = 0.05
sample_size = len(results_df)
power_analysis = TTestIndPower()

# Calculate power
power = power_analysis.power(effect_size=effect_size, nobs1=sample_size, alpha=alpha)
print(f"Calculated Power: {power:.4f}")

# Plot power vs. sample size (limited range)
sample_sizes = np.arange(10, 500, 10)  # Adjust the upper limit as needed
powers = [power_analysis.power(effect_size=effect_size, nobs1=n, alpha=alpha) for n in sample_sizes]

plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, powers, marker='o')
plt.title('Power Analysis (Limited Range)')
plt.xlabel('Sample Size')
plt.ylabel('Power')
plt.grid(True)
# Save the plot as a PNG file
plot_filename = 'power_analysis_plot_limited.png'
plt.savefig(plot_filename)
print(f"Power analysis plot saved as {plot_filename}")
