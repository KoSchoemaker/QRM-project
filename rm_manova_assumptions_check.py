import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.anova import AnovaRM

# Merging datasets based on patient_id and date
merged_df = sleep_df.merge(demographics_df, on='patient_id', how='left')
merged_df = merged_df.merge(activity_df, on=['patient_id', 'date'], how='left')
merged_df = merged_df.merge(physiology_df, on=['patient_id', 'date'], how='left')
merged_df = merged_df.merge(labels_df, on=['patient_id', 'date'], how='left')

# Display the merged dataframe structure
merged_df.head()

# Checking for Multivariate Normality
dependent_vars = ['heart_rate', 'respiratory_rate', 'snoring']  # Replace with actual dependent variables
for var in dependent_vars:
    stat, p = stats.shapiro(merged_df[var].dropna())
    print(f'Shapiro-Wilk test for {var}: Statistics={stat}, p={p}')
    sns.histplot(merged_df[var].dropna(), kde=True)
    plt.title(f'Histogram of {var}')
    plt.show()

# Checking for Sphericity
# Example with AnovaRM (statsmodels)
# Convert date to categorical day number for within-subject factor
merged_df['day'] = pd.to_datetime(merged_df['date']).dt.day

# Run Repeated Measures ANOVA as a preliminary step to check sphericity
aovrm = AnovaRM(merged_df, depvar='heart_rate', subject='patient_id', within=['day'])
res = aovrm.fit()
print(res)

# Checking for Equality of Covariance Matrices (Box's M test)
# Function for Box's M test
from statsmodels.multivariate.cancorr import CanCorr

def box_m_test(data, group_col, dep_vars):
    groups = data[group_col].unique()
    grouped_data = [data[data[group_col] == g][dep_vars].values for g in groups]
    n_groups = len(groups)
    n_vars = len(dep_vars)
    n_total = sum([len(g) for g in grouped_data])
    
    pooled_cov = sum([(len(g) - 1) * np.cov(g, rowvar=False) for g in grouped_data]) / (n_total - n_groups)
    log_det_pooled_cov = np.log(np.linalg.det(pooled_cov))
    
    log_dets = [np.log(np.linalg.det(np.cov(g, rowvar=False))) for g in grouped_data]
    group_sizes = [len(g) for g in grouped_data]
    
    M = (n_total - n_groups) * log_det_pooled_cov - sum([(size - 1) * det for size, det in zip(group_sizes, log_dets)])
    correction_factor = (2 * n_vars ** 2 + 3 * n_vars - 1) * (n_groups - 1) / (6 * (n_vars + 1) * (n_total - n_groups))
    chi_square = M * (1 - correction_factor)
    df = 0.5 * n_vars * (n_vars + 1) * (n_groups - 1)
    p_value = 1 - stats.chi2.cdf(chi_square, df)
    
    return chi_square, p_value

# Perform Box's M test
chi_square, p_value = box_m_test(merged_df, 'patient_id', dependent_vars)
print(f"Box's M test: Chi-square={chi_square}, p-value={p_value}")

