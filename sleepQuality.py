import pandas as pd
import plotting

def getSleepWakeDateTimes(patientEvents):
    
    # interval to be considered wake and sleep moment
    minimumInterval = 3600*3 # three hours

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
            sleepWakeDateTimePair.append((previousSleepTime, previousEvent.date))
            previousSleepTime = event.date
        previousEvent = event

    return sleepWakeDateTimePair

def getSleepQuality(sleepDataFrame, patientId):
    sleepDataFrame['date'] = pd.to_datetime(sleepDataFrame['date'])
    patientEvents = sleepDataFrame[sleepDataFrame['patient_id'] == patientId]

    sleepWakeDateTimePair = getSleepWakeDateTimes(patientEvents)

    maximumInterval = 3600*3
    monitorStates = sleepDataFrame.state.unique()
    recordedEvents = {key: [] for key in monitorStates}
    wasos=[]
    latencies=[]
    

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
        latencies.append(wasoDuration)
        wasos.append(sleepLatencyDuration)

    recordedEvents = {key: int(sum(value)) for key, value in recordedEvents.items()}
    # print(recordedEvents)
    # print(sum(list(recordedEvents.values())))
    # plotting.latencyplot(latencies)
    # plotting.latencyplot(wasos)

    # metric

    sleepPeriod = recordedEvents['LIGHT'] + recordedEvents['DEEP'] + recordedEvents['REM']
    efficiency = (sleepPeriod - sum(wasos)) / (sleepPeriod + sum(latencies))
    return efficiency

def getPatientMetrics(patientSleep):
    # get values for one patients
    return []

def getSleepEfficiency(patientSleep):
    # Total sleep time to time in bed ratio
    pass

def getSleepLatency(patientSleep):
    # Time in minutes to transition from awake to sleep
    pass

def getREMDistribution(patientSleep):
    # Ratio of REM time to total sleep time
    pass

def getLightSleepDistribution(patientSleep):
    # Total sleep time to time in bed ratio
    pass

def getDeepSleepDistribution(patientSleep):
    # Ratio of Deep sleep time to total sleep time
    pass

def getAwakenings(patientSleep):
    # Number of times in which individuals became awake, >5 min
    pass

def getWakeAfterSleepOnset(patientSleep):
    # Time spent awake after sleep has started and before final wake-up
    pass