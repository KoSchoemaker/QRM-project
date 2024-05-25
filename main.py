# imports
import pandas as pd
import os
import os.path
from sleepSchedule import getSleepVariance

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
print('-> filesystem intact')

# reading csv file
activityDataFrame = pd.read_csv(activityPath)
sleepDataFrame = pd.read_csv(sleepPath)
demographicsDataFrame = pd.read_csv(demographicsPath)

# get a list of all patientIds
patientIds = demographicsDataFrame[['patient_id']].to_numpy().flatten()

# only consider participants that have both sleep and activity data
patientIds = [id for id in patientIds if id in sleepDataFrame[['patient_id']].values and id in activityDataFrame[['patient_id']].values]

# TODO remove participants with less that x sleep data

# patientIds = [patientIds[4]] # for now just use one participant. comment line for loop over all participants
for i, patientId in enumerate(patientIds):
    print(f'-> processing patientID {i}: {patientId}')
    sleepVariance = getSleepVariance(sleepDataFrame, patientId)
    print(f'sleepVariance= {sleepVariance}')