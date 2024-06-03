import ciso8601
import numpy as np
import datetime

import plotting
import dataAnalysis

def toTimeSinceMidnight(timestampList):
    if len(timestampList) == 0:
        return []
    dt = datetime.datetime.fromtimestamp(timestampList[0])
    dayStart = datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0).timestamp()

    return [timestamp - dayStart for timestamp in timestampList]

def getRoomUsage(activityDataframe, patientId):
    # activityDataframe[patientId]
    # define thresholds: minimum event duration, 
    # get all types of activities for this patient (EXCLUDING backdoor, frontdoor, fridgedoor)
    # for every event in patients activity
    #   record start time
    #   if event type == previous event type
    #       continue loop
    #   if different event type
    #       figure out duration of this new event
    #       if this event longer than x minutes
    #           there is a new event. record start time of this new event and continue loop again
    # save everything to a dict {'bathroom': list of <float>([startTime1, starttime2 etc]}

    # Q: what to do with non-activity (no events) for a long time? are they in same room as previous event?
    #   A: I think at least x observations are needed within the entire time before we can determine they're in a room 
    # Q: should we take sleep schedule into account? because then we know theyre bedroom
    #   A: I think not because we're already measuring sleep schedule, maybe double data

    activities = activityDataframe.location_name.unique()
    activities = [act for act in activities if act not in ['Fridge Door', 'Front Door', 'Back Door']]
    patientActivities = activityDataframe[activityDataframe['patient_id'] == patientId]
    
    recordedEvents = {key: [] for key in activities}

    previousEvent = None
    startEvent = None
    eventDuration = 0
    for event in patientActivities.itertuples():
        # exclude some activities from monitoring
        if event.location_name not in activities:
            continue
        # first iteration in the loop, no previous event yet, so record and continue
        if previousEvent == None:
            recordedEvents[event.location_name].append(event.date)
            previousEvent = event
            startEvent = previousEvent
            continue
        if previousEvent.location_name == event.location_name:
            # eventDuration = eventDuration + (pd.to_datetime(event.date) - pd.to_datetime(previousEvent.date)).total_seconds()
            continue
        startUnix = ciso8601.parse_datetime(startEvent.date)
        timeDelta = (ciso8601.parse_datetime(event.date) - startUnix).total_seconds()
        eventDuration = eventDuration + timeDelta
        startTimestamp = startUnix.timestamp()
        recordedEvents[startEvent.location_name].extend(range(int(startTimestamp), int(startTimestamp + eventDuration)))
        startEvent = event
        previousEvent = event
        eventDuration = 0
    # plotting.roomUsageBinaryDay(recordedEvents, patientId)

    return recordedEvents

def getRoomUsageVariance(activityDataframe, patientId, plotCircle=False):
    timesDict = getRoomUsage(activityDataframe, patientId)
    circularVarianceDict = dataAnalysis.getCircularVarianceFromDict(timesDict)
    if plotCircle:
        plotting.roomUsageCircle(timesDict, patientId)
    return circularVarianceDict