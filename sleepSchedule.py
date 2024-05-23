import pandas as pd

def getSleepSchedule(sleepDataFrame, patientId):
    # a pd series with all datetimes of sleep data from the patient
    patientSleepTimes = pd.to_datetime(sleepDataFrame[sleepDataFrame['patient_id'] == patientId]['date'])

    # no sleep data
    if len(patientSleepTimes) == 0:
        print('-> no sleep data for patient')
        return ([],[])
    
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
            wakeTimes.append(prevData.hour + (prevData.minute / 60))
            sleepTimes.append(data.hour + (data.minute / 60))
            # print(f'wake time {prevData}, next sleep time {data}')
        prevData = data

    return (wakeTimes, sleepTimes)

# TODO normalize days (only look at times, perhaps using just a number of seconds/minutes into the day)
# TODO exclude naps?
# TODO compare values (measure variance?)