import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotting
from cmath import rect, phase
from math import radians, degrees

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

# TODO normalize days (only look at times, perhaps using just a number of seconds/minutes into the day)
# TODO exclude naps
# TODO compare values (measure variance?)

def getTimesAngles(times):
    return np.array([((h * 60 + m) / (24 * 60)) * 2 * np.pi for h,m in times])

def getCircularVariance(times):
    angles = getTimesAngles(times)

    # Calculate the mean resultant length
    C = np.mean(np.cos(angles))
    S = np.mean(np.sin(angles))
    R = np.sqrt(C**2 + S**2)

    # Calculate the circular variance
    circular_variance = 1 - R
    return circular_variance

def getSleepVariance(sleepDataFrame, patientId, plotCircle = False):
    wakeSchedule, sleepSchedule = getSleepSchedule(sleepDataFrame, patientId)
    wakeCircularVariance = getCircularVariance(wakeSchedule)
    sleepCircularVariance = getCircularVariance(sleepSchedule)
    if plotCircle:
        plotting.wakeSleepCircle(wakeSchedule, sleepSchedule, patientId)
    return (wakeCircularVariance, sleepCircularVariance)

# depricated
def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg)/len(deg)))

# depricated
def mean_time(times):
    seconds = ((float(s) + int(m) * 60 + int(h) * 3600) for h, m, s in times)
    day = 24 * 60 * 60
    to_angles = [s * 360. / day for s in seconds]
    mean_as_angle = mean_angle(to_angles)
    mean_seconds = mean_as_angle * day / 360.
    if mean_seconds < 0:
        mean_seconds += day
    h, m = divmod(mean_seconds, 3600)
    m, s = divmod(m, 60)
    return '%02i:%02i:%02i' % (h, m, s)