# QRM-project
Using TIHM dataset, try to figure out to what extend routine influences sleep quality

## Setup
In the *TIHM_Dataset* folder, paste the unzipped dataset csv files which can be found [here](https://zenodo.org/records/7622128).

## Directories
- the *intermediate_results* folder contains json files with some results that can be used for further analysis. This exists so not all code has to be ran to do some further analysis (running all code may take quite some time!).
- *figures* contains figures of interesting patterns seen in the data
- *old* contains deprecated code files that are not used for the final main analysis, but was used in the process.

## File structure
- *main.py* contains all logic to calculate the IVs and DVs for this project.
- *clustering.py* contains logic for clustering participants based on intermediate results
- all other files should not be executed by theselves, but are used by the above listed files in one way or another. They exist to create a more logical structure to the code.