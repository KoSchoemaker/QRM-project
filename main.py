# imports
import pandas as pd

import fileIntegrity
import patientSelection
from sleepSchedule import getSleepVariance
from roomUsage import getRoomUsageVariance

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

# patientIds = [patientIds[4]] # for now just use one participant. comment line for loop over all participants
for i, patientId in enumerate(patientIds):
    print(f'-> processing patientID {i}: {patientId}')
    sleepVariance = getSleepVariance(sleepDataFrame, patientId)
    print(f'sleepVariance= {sleepVariance}')
    # TODO roomUsage.getRoomUsageVariances(activityDataframe, patientId), returns {bathroom: float bedroom: float etc.}
    roomUsageVariance = getRoomUsageVariance(activityDataFrame, patientId)
    print(f'roomUsageVariance= {roomUsageVariance}')
    # DONE dataAnalysis.getVarianceSum(sleepVariance: dict, roomUsageVariance: dict), returns float
    # TODO K-means clustering using elbow method OR hierarchal clustering or subjects using accumulated variance
    #   https://www.geeksforgeeks.org/elbow-method-for-optimal-value-of-k-in-kmeans/
    #   https://stackoverflow.com/questions/10136470/unsupervised-clustering-with-unknown-number-of-clusters

    # TODO sleep quality DVs