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
activityDataFrame['date'] = pd.to_datetime(activityDataFrame['date'])

sleepDataFrame = pd.read_csv(sleepPath)
sleepDataFrame['date'] = pd.to_datetime(sleepDataFrame['date'])

demographicsDataFrame = pd.read_csv(demographicsPath)

# get a list of all patientIds
patientIds = patientSelection.getPatientIds(demographicsDataFrame, sleepDataFrame, activityDataFrame)
# patientIds = [patientIds[1]] # use just one participant. comment line for loop over all participants

sleepEfficiencyPatientDict = {}
roomUsageSleepSchedulePatientDict = {}
variableDict = {}
for i, patientId in enumerate(patientIds):
    print(f'-> processing patientID {i}: {patientId}')
    patientSleepDataFrame = sleepDataFrame[sleepDataFrame['patient_id'] == patientId]

    # IV sleep variance
    sleepVariance = getSleepVariance(patientSleepDataFrame, patientId)
    print(f'sleepVariance= {sleepVariance}')

    # IV room usage
    roomUsageDice = getRoomUsageMetric(activityDataFrame, patientId)
    print(f'roomUsageDice= {roomUsageDice}')

    # DV sleep quality
    totalSleepTime, totalMinutesInBed = getSleepQuality(patientSleepDataFrame, patientId)
    sleepEfficiency = totalSleepTime / totalMinutesInBed
    print(f'sleepEfficiency= {sleepEfficiency}')

    sleepEfficiencyPatientDict[patientId] = {'sleepEfficiency': sleepEfficiency, 'totalSleepTime': totalSleepTime, 'totalMinutesInBed': totalMinutesInBed}
    roomUsageSleepSchedulePatientDict[patientId] = {'roomUsageDiceMean': np.mean(list(roomUsageDice.values())), 'sleepScheduleVarianceSum': np.sum(list(sleepVariance.values()))}
    variableDict[patientId] = {'sleepSchedule': sleepVariance, 'roomUsage': roomUsageDice, 'totalSleepTime': totalSleepTime, 'totalMinutesInBed': totalMinutesInBed, 'sleepEfficiency': sleepEfficiency}

fileIntegrity.writeJson(sleepEfficiencyPatientDict, 'efficiencies')
fileIntegrity.writeJson(roomUsageSleepSchedulePatientDict, 'room_usage_mean_sleep_schedule_sum')
fileIntegrity.writeJson(variableDict, 'variables')