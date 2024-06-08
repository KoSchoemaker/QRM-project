import pandas as pd

def getSleepWakeDateTimes(patientEvents):
    
    # interval to be considered wake and sleep moment
    minimumInterval = 3600*3 # three hours

    # minimum time a participant needs to be asleep to consider it sleep. Exists to exclude naps
    minimumSleepTime = 3600*3 # three hours

    previousEvent = None
    previousSleepTime = None
    sleepWakeDateTimePair = []
    for event in patientEvents.itertuples():
        if previousEvent is None:
            previousEvent = event
            previousSleepTime = event.date
            continue
        
        delta = event.date-previousEvent.date
        if delta.total_seconds() > minimumInterval:
            sleepDuration = (previousEvent.date - previousSleepTime).total_seconds()
            if sleepDuration > minimumSleepTime:
                sleepWakeDateTimePair.append((previousSleepTime, previousEvent.date))
            previousSleepTime = event.date
        previousEvent = event

    return sleepWakeDateTimePair

def getSleepQuality(sleepDataFrame, patientId):
    sleepDataFrame['date'] = pd.to_datetime(sleepDataFrame['date'])
    patientEvents = sleepDataFrame[sleepDataFrame['patient_id'] == patientId]

    sleepWakeDateTimePair = getSleepWakeDateTimes(patientEvents)

    maximumInterval = 3600*3
    wasoMinimumThreshold = 5*60 #5 minutes
    monitorStates = sleepDataFrame.state.unique()
    recordedEvents = {key: [] for key in monitorStates}
    wasoDurationList=[]
    sleepLatencyDurationList=[]

    # for each day
    for sleep, wake in sleepWakeDateTimePair:
        mask = (patientEvents['date'] > sleep) & (patientEvents['date'] <= wake)
        patientDayEvents = patientEvents.loc[mask]

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
