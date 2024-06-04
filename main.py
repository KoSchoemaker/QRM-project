# imports
import pandas as pd
import numpy as np

import fileIntegrity
import patientSelection
from sleepSchedule import getSleepVariance
from roomUsage import getRoomUsageMetric

# filePaths
activityPath = 'TIHM_Dataset/Activity.csv'
sleepPath = 'TIHM_Dataset/Sleep.csv'
demographicsPath = 'TIHM_Dataset/Demographics.csv'

# check if needed files exist
fileIntegrity.checkFiles(activityPath, sleepPath, demographicsPath)

# reading csv file
activityDataFrame = pd.read_csv(activityPath)
sleepDataFrame = pd.read_csv(sleepPath)
demographicsDataFrame = pd.read_csv(demographicsPath)

# get a list of all patientIds
patientIds = patientSelection.getPatientIds(demographicsDataFrame, sleepDataFrame, activityDataFrame)
roomusagedict = {}
# patientIds = [patientIds[4]] # for now just use one participant. comment line for loop over all participants
for i, patientId in enumerate(patientIds):
    print(f'-> processing patientID {i}: {patientId}')
    sleepVariance = getSleepVariance(sleepDataFrame, patientId)
    print(f'sleepVariance= {sleepVariance}')
    roomUsageDice = getRoomUsageMetric(activityDataFrame, patientId)
    print(f'roomUsageDice= {roomUsageDice}')
    roomUsageMean = np.mean(list(roomUsageDice.values()))
    print(f'roomUsageDiceMean= {roomUsageMean}')
    roomusagedict[patientId] = (roomUsageMean, np.sum(list(sleepVariance.values())))
    # TODO sleep quality DVs
    
import json
with open('intermediate_results/roomusagemean_sleepsum_results.json', 'w') as f:
    json.dump(roomusagedict, f)