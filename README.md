# QRM-project
Using TIHM dataset, try to figure out to what extend routine influences sleep quality

## Setup
In the *TIHM_Dataset* folder, paste the unzipped dataset csv files which can be found [here](https://zenodo.org/records/7622128).

## How to run this?
1. Make sure you have put the required TIHM CSV files in the TIHM_Dataset directory.
2. run *main.py* to perform preprocessing. Running this will analyse the data and create results for every participant's summed sleep schedule, mean room usage and mean sleep efficiency. These results will be written to intermediate_results/room_usage_mean_sleep_schedule_sum.json, intermediate_results/efficiencies.json and intermediate_results/variables.json
3. run *clustering.py* to use the summed sleep schedule and mean room usage saved to intermediate_results/room_usage_mean_sleep_schedule_sum.json to cluster participants into clusters of 'routine' and 'no routine'. Results of clustering are saved to intermediate_results/patient_clustering_results_bigger_sample.json
4. run *assumptions_test.py* to perform the parametric assumptions tests, running this will perform Shapiro-Wilk's test for normality and Levene's homogeneity of variances test on sleep efficiency variables found in intermediate_results/efficiencies.json and group clusters found in intermediate_results/patient_clustering_results_bigger_sample.json. This will also create Q-Q plots of the data. Shapiro-Wilk and Levene's test results are written to assumptions_test_results/assumption_tests_results.json and Q-Q plots to assumptions_test_results/qq_plot_{routine}.png.
5. run *welch_t_test.py* to perform the Welch's t-test on the 'routine' and 'no routine' groups found in intermediate_results/patient_clustering_results_bigger_sample.json and the sleep efficiency variable found in intermediate_results/efficiencies.json. The effect size, using Cohen's d tes, and statistical power will also be calculated. Results are saved to analysis/welch_test_results.json.
6. run *multivariate_regression.py* to perform post hoc analysis on the individual independent variables that make up mean sleep schedule and mean room usage along with the dependent variables total sleep time and total minutes in bed. The multivariate regression will use intermediate_results/variables.json to pull both IVs and DVs. Results are written in post_hoc/multivariate_regression_totalSleepTime_summary.txt and post_hoc/multivariate_regression_totalMinutesInBed_summary.txt.

## Directories
- the *intermediate_results* folder contains json files with some results that can be used for further analysis. This exists so not all code has to be ran to do some further analysis (running all code may take quite some time!).
- *figures* contains figures of interesting patterns seen in the data
- *old* contains deprecated code files that are not used for the final main analysis, but was used in the process.

## File structure
- *main.py* contains all logic to calculate the IVs and DVs for this project.
- *clustering.py* contains logic for clustering participants based on intermediate results
- *plotting_standalone.py* contains code for creating plots, some of which were used for the report. *plotting.py* also creates plots, but is used by switching the plotting variable to True in *main.py*
- all other files should not be executed by theselves, but are used by the above listed files in one way or another. They exist to create a more logical structure to the code.