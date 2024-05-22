# imports
import pandas as pd
import os
import os.path

def checkFile(filePath):
    if not (os.path.isfile(filePath) and os.access(filePath, os.R_OK)):
        raise FileExistsError(f'check if {filePath} is readable and intact')

# filePaths
activityPath = 'TIHM_Dataset/Activity.csv'
sleepPath = 'TIHM_Dataset/Sleep.csv'
demographicsPath = 'TIHM_Dataset/Demographics.csv'

# check if needed files exist
checkFile(activityPath)
checkFile(sleepPath)
checkFile(demographicsPath)
print('->filesystem intact')

# reading csv file
sleepDataFrame = pd.read_csv(sleepPath)
print(sleepDataFrame.head())

# IVs
## for a patient (because we're doing within-subject design):
### for each day:
#### get sleep schedule (first time sleep.csv registered and last time it was registered for a certain sleep period)
### analyse data and create metric for consistency: get variance (?) for these two variables