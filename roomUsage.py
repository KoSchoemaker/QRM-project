import ciso8601

import plotting
import dataAnalysis

""" method returns a dictionary with all times a person occupied a room. Every second is counted (interpolated) {'roomName': [unix1, unix2, unix3...]}"""
def getRoomUsage(activityDataframe, patientId):

    # make a list of all locations we are interested in monitoring
    monitorLocations = activityDataframe.location_name.unique()
    monitorLocations = [act for act in monitorLocations if act not in ['Fridge Door', 'Front Door', 'Back Door']]

    # create a dataframe with only activities for the current patient
    patientActivities = activityDataframe[activityDataframe['patient_id'] == patientId]
    
    recordedEvents = {key: [] for key in monitorLocations}
    previousEvent = None
    startEvent = None
    eventDuration = 0
    for event in patientActivities.itertuples():
        # exclude some activities from monitoring
        if event.location_name not in monitorLocations:
            continue
        # first iteration in the loop, no previous event yet, so record and continue
        if previousEvent == None:
            previousEvent = event
            startEvent = previousEvent
            continue
        if previousEvent.location_name == event.location_name:
            previousEvent = event
            continue
        startUnix = ciso8601.parse_datetime(startEvent.date)
        timeDelta = (ciso8601.parse_datetime(event.date) - startUnix).total_seconds()
        eventDuration = eventDuration + timeDelta
        startTimestamp = startUnix.timestamp()
        recordedEvents[startEvent.location_name].extend(range(int(startTimestamp), int(startTimestamp + eventDuration)))
        startEvent = event
        previousEvent = event
        eventDuration = 0

    return recordedEvents

def getRoomUsageMetric(activityDataframe, patientId, plotCircle=False):
    timesDict = getRoomUsage(activityDataframe, patientId)
    circularVarianceDict = dataAnalysis.getDiceFromDict(timesDict)
    if plotCircle:
        # plotting.roomUsageCircle(timesDict, patientId)
        plotting.roomUsageBinaryDay(timesDict, patientId)
    return circularVarianceDict