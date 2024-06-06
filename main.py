# imports
import pandas as pd
import numpy as np

import fileIntegrity
import patientSelection
from sleepSchedule import getSleepVariance
from roomUsage import getRoomUsageMetric
from sleepQuality import getSleepQuality

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
# patientIds = [patientIds[1]] # for now just use one participant. comment line for loop over all participants

efficiencies = {}
roomusagedict = {}
for i, patientId in enumerate(patientIds):
    print(f'-> processing patientID {i}: {patientId}')

    # sleepVariance = getSleepVariance(sleepDataFrame, patientId)
    # print(f'sleepVariance= {sleepVariance}')

    # roomUsageDice = getRoomUsageMetric(activityDataFrame, patientId)
    # print(f'roomUsageDice= {roomUsageDice}')

    sleepEfficiency, totalSleepTime, totalMinutesInBed = getSleepQuality(sleepDataFrame, patientId)
    print(f'sleepQuality= {sleepEfficiency}')
    efficiencies[patientId] = sleepEfficiency
    # roomUsageMean = np.mean(list(roomUsageDice.values()))
    # sleepScheduleSum = np.sum(list(sleepVariance.values()))
    # roomusagedict[patientId] = (roomUsageMean, sleepScheduleSum)
    
# import json
# with open('intermediate_results/room_usage_mean_sleep_schedule_sum_results.json', 'w') as f:
#     json.dump(roomusagedict, f)

import json
with open('intermediate_results/efficiencies.json', 'w') as f:
    json.dump(efficiencies, f)