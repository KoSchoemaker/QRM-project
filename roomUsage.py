import plotting
import dataAnalysis

# TODO implement
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
    return {}

def getRoomUsageVariance(activityDataframe, patientId, plotCircle=False):
    timesDict = getRoomUsage(activityDataframe, patientId)
    circularVarianceDict = dataAnalysis.getCircularVarianceFromDict(timesDict)
    if plotCircle:
        plotting.roomUsageCircle(timesDict, patientId)
    return circularVarianceDict