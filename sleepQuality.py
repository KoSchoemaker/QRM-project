import pandas as pd
import plotting

def getSleepQuality(sleepDataFrame, patientId):
    # loop over patients, give patient sleep data, create dataframe with info for all patients
    sleepDataFrame['date'] = pd.to_datetime(sleepDataFrame['date'])
    patientData = sleepDataFrame[sleepDataFrame['patient_id'] == patientId]

    minimumInterval = 3600*3 # three hours

    prevData = None
    wakeTimes = []
    prevSleepTime = None
    sleepTimes = []
    sleepPairs = []
    for data in patientData.itertuples():
        if prevData is None:
            prevData = data
            prevSleepTime = data.date
            continue
        
        delta = data.date-prevData.date
        if delta.total_seconds() > minimumInterval:
            wakeTimes.append(prevData.date)
            sleepTimes.append(data.date)
            sleepPairs.append((prevSleepTime, prevData.date))
            prevSleepTime = data.date
        prevData = data
    # offset = 0
    # if wakeTimes[0] < sleepTimes[0]:
    #     offset = 1

    maximumInterval = 3600*3
    monitorStates = sleepDataFrame.state.unique()
    recordedEvents = {key: [] for key in monitorStates}
    wasos=[]
    latencies=[]

    for sleep, wake in sleepPairs:
        mask = (patientData['date'] > sleep) & (patientData['date'] <= wake)
        patientDayData = patientData.loc[mask]

        previousEvent = None
        startEvent = None
        startWaso = None
        waso = 0
        latency = 0
        for event in patientDayData.itertuples():
            if previousEvent == None:
                previousEvent = event
                startEvent = previousEvent
                if event.state == 'AWAKE':
                    startWaso = event
                continue
            if previousEvent.state == event.state:
                # eventDuration = (event.date - previousEvent.date).total_seconds()

                # # not needed anymore
                # # if eventDuration > maximumInterval:
                # #     eventDuration = (previousEvent.date - startEvent.date).total_seconds()
                # #     recordedEvents[startEvent.state].append(eventDuration)
                # #     startEvent = event
                previousEvent = event
                continue
            if startWaso is not None:
                wasoDuration = (event.date - startWaso.date).total_seconds()
                waso = wasoDuration
                

            if startWaso == None and previousEvent.state == 'AWAKE':
                eventDuration = (event.date - startEvent.date).total_seconds()
                latency = latency + eventDuration

            eventDuration = (event.date - previousEvent.date).total_seconds()
            if eventDuration > maximumInterval:
                eventDuration = (previousEvent.date - startEvent.date).total_seconds()
            else: 
                eventDuration = (event.date - startEvent.date).total_seconds()
            recordedEvents[startEvent.state].append(eventDuration)
            startEvent = event
            previousEvent = event
            startWaso = None
        latencies.append(latency)
        wasos.append(waso)

    recordedEvents = {key: int(sum(value)) for key, value in recordedEvents.items()}
    # print(recordedEvents)
    # print(sum(list(recordedEvents.values())))
    # plotting.latencyplot(latencies)
    # plotting.latencyplot(wasos)

    # metric

    print(recordedEvents)
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