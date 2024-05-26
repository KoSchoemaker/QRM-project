import plotting
import dataAnalysis

# TODO implement
def getRoomUsage(activityDataframe, patientId):
    return {}

def getRoomUsageVariance(activityDataframe, patientId, plotCircle=False):
    timesDict = getRoomUsage(activityDataframe, patientId)
    circularVarianceDict = dataAnalysis.getCircularVarianceFromDict(timesDict)
    if plotCircle:
        plotting.roomUsageCircle(timesDict, patientId)
    return circularVarianceDict