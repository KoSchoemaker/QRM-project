import pandas as pd

def getSleepSchedule(sleepDataFrame, patientId):
    # a pd series with all datetimes of sleep data from the patient
    patientSleepTimes = pd.to_datetime(sleepDataFrame[sleepDataFrame['patient_id'] == patientId]['date'])

    timeThreshold = 3600*3 # three hours
    prevData = None
    wakeTimes = []
    sleepTimes = []
    for index, data in patientSleepTimes.items():
        if prevData == None:
            prevData = data
            continue
        
        delta = data-prevData
        if delta.total_seconds() > timeThreshold:
            wakeTimes.append(prevData)
            sleepTimes.append(data)
            # print(f'wake time {prevData}, next sleep time {data}')
        prevData = data

    return (wakeTimes, sleepTimes)

# TODO normalize days (only look at times, perhaps using just a number of seconds/minutes into the day)
# TODO compare values (measure variance?)