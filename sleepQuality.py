import pandas as pd
import datetime

def getSleepWakeDateTimes(patientEvents):
    
    # interval to be considered wake and sleep moment
    minimumInterval = 3600*3 # three hours

    # minimum time a participant needs to be asleep to consider it sleep. Exists to exclude naps
    minimumSleepTime = 3600*3 # three hours

    firstDataSetEvent = datetime.datetime(2019, 4, 1, 0, 10) # 2019-04-01 00:00:00
    lastDataSetEvent = datetime.datetime(2019, 6, 30, 23, 50) # 2019-06-30 23:59:00

    previousEvent = None
    previousSleepTime = None
    sleepWakeDateTimePair = []
    for event in patientEvents.itertuples():
        if previousEvent is None:
            previousEvent = event
            previousSleepTime = event.date
            continue
        
        wakeTime = previousEvent.date
        delta = event.date-wakeTime
        if delta.total_seconds() > minimumInterval:
            sleepDuration = (wakeTime - previousSleepTime).total_seconds()
            if sleepDuration > minimumSleepTime and previousSleepTime > firstDataSetEvent and wakeTime < lastDataSetEvent:
                sleepWakeDateTimePair.append((previousSleepTime, wakeTime))
            previousSleepTime = event.date
        previousEvent = event
    if previousSleepTime > firstDataSetEvent and wakeTime < lastDataSetEvent:
        sleepWakeDateTimePair.append((previousSleepTime, wakeTime)) # last day not counted because of sudden stop of data on 2019-06-30 23:59:00
    return sleepWakeDateTimePair

def getSleepQuality(patientSleepDataFrame, patientId):
    sleepWakeDateTimePair = getSleepWakeDateTimes(patientSleepDataFrame)

    maximumInterval = 3600*3
    wasoMinimumThreshold = 5*60 #5 minutes
    monitorStates = patientSleepDataFrame.state.unique()
    recordedEvents = {key: [] for key in monitorStates}
    wasoDurationList=[]
    sleepLatencyDurationList=[]

    # for each day
    for sleep, wake in sleepWakeDateTimePair:
        mask = (patientSleepDataFrame['date'] > sleep) & (patientSleepDataFrame['date'] <= wake)
        patientDayEvents = patientSleepDataFrame.loc[mask]

        previousEvent = None
        startEvent = None
        startOfSleepLatency = None
        wasoDuration = 0
        sleepLatencyDuration = 0
        # for each event on this day
        for event in patientDayEvents.itertuples():
            if previousEvent == None:
                previousEvent = event
                startEvent = previousEvent
                if event.state == 'AWAKE':
                    startOfSleepLatency = event
                continue
            if previousEvent.state == event.state:
                previousEvent = event
                continue
            if startOfSleepLatency is not None:
                sleepLatencyDuration = (event.date - startOfSleepLatency.date).total_seconds()
                
            if startOfSleepLatency == None and previousEvent.state == 'AWAKE':
                eventDuration = (event.date - startEvent.date).total_seconds()
                if eventDuration > wasoMinimumThreshold:
                    wasoDuration = wasoDuration + eventDuration

            eventDuration = (event.date - previousEvent.date).total_seconds()
            if eventDuration > maximumInterval:
                eventDuration = (previousEvent.date - startEvent.date).total_seconds()
            else: 
                eventDuration = (event.date - startEvent.date).total_seconds()
            recordedEvents[startEvent.state].append(eventDuration)
            startEvent = event
            previousEvent = event
            startOfSleepLatency = None
        wasoDurationList.append(wasoDuration)
        sleepLatencyDurationList.append(sleepLatencyDuration)

    recordedEvents = {key: int(sum(value)) for key, value in recordedEvents.items()}

    totalWASODuration = sum(wasoDurationList)
    totalSleepLatencyDuration = sum(sleepLatencyDurationList)
    sleepPeriod = recordedEvents['LIGHT'] + recordedEvents['DEEP'] + recordedEvents['REM'] + totalWASODuration

    totalSleepTime = sleepPeriod - totalWASODuration
    totalMinutesInBed = sleepPeriod + totalSleepLatencyDuration

    sleepEfficiency = totalSleepTime / totalMinutesInBed
    print(f'sleepperiod {sleepPeriod/60}, wasos {totalWASODuration/60}, latency {totalSleepLatencyDuration/60}')

    return sleepEfficiency, totalSleepTime, totalMinutesInBed
