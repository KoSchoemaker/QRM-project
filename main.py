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
activityDataFrame = pd.read_csv(activityPath)
sleepDataFrame = pd.read_csv(sleepPath)
demographicsDataFrame = pd.read_csv(demographicsPath)

# get a list of all patientIds
patientIDs = demographicsDataFrame[['patient_id']].to_numpy().flatten()

print(sleepDataFrame.head())

# later make a loop, for now just use one participant
patientId = patientIDs[0]

# IVs
## for a patient (because we're doing within-subject design):
### for each day:
#### get sleep schedule (first time sleep.csv registered and last time it was registered for a certain sleep period)
### analyse data and create metric for consistency: get variance (?) for these two variables