import pandas as pd

import plotting
import dataAnalysis
import sleepQuality

def getSleepSchedule(sleepDataFrame, patientId):
    # a pd series with all DateTime obj of sleep data from the patient
    patientSleepTimes = pd.to_datetime(sleepDataFrame[sleepDataFrame['patient_id'] == patientId]['date'])

    # no sleep data. should already have been filtered out in main.py
    if len(patientSleepTimes) == 0:
        print('-> no sleep data for patient')
        return ([],[])
    
    # the minimum time between one and another sleep event. If two subsequent events are further apart than this value,
    #   count as separate events, so record a wake and sleep time for this.
    minimumInterval = 3600*3 # three hours

    # the minimum duration that sleep has to occur for us to record it as such. This mainly exists to filter out
    #   naps during the daytime
    minimumDuration = 3600*2 # two hours TODO
    # TODO exclude naps

    prevData = None
    wakeTimes = []
    sleepTimes = []
    for index, data in patientSleepTimes.items():
        if prevData == None:
            prevData = data
            continue
        
        delta = data-prevData
        if delta.total_seconds() > minimumInterval:
            wakeTimes.append((prevData.hour, prevData.minute))
            sleepTimes.append((data.hour, data.minute))
        prevData = data

    return (wakeTimes, sleepTimes)

def convertToSleepWakeTime(sleepWakeDateTimePair):
    return [(pair[0].hour, pair[0].minute) for pair in sleepWakeDateTimePair], [(pair[1].hour, pair[1].minute) for pair in sleepWakeDateTimePair]

def getSleepVariance(patientSleepDataFrame, patientId, plotCircle = False):

    # method 2 better
    sleepWakeDateTimePair = sleepQuality.getSleepWakeDateTimes(patientSleepDataFrame)
    sleepSchedule, wakeSchedule = convertToSleepWakeTime(sleepWakeDateTimePair)

    # method 1 depricated
    # wakeSchedule, sleepSchedule = getSleepSchedule(sleepDataFrame, patientId)

    wakeCircularVariance = dataAnalysis.getCircularVariance(wakeSchedule)
    sleepCircularVariance = dataAnalysis.getCircularVariance(sleepSchedule)
    if plotCircle:
        plotting.wakeSleepCircle(wakeSchedule, sleepSchedule, patientId, wakeCircularVariance, sleepCircularVariance)
    return {'wake': wakeCircularVariance, 'sleep': sleepCircularVariance}