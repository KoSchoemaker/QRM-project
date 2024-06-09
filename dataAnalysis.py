import numpy as np

def getDayEvents(timesList, dayStart):
    return [time for time in timesList if time > dayStart and time < dayStart + 86400]

def toTimeSinceMidnight(timestampList, dayStart):
    if len(timestampList) == 0:
        return []

    return [timestamp - dayStart for timestamp in timestampList]

def getDiceCoefficient(timesList):
    diceValues = []
    previousDay = None

    # from first day in experiment until last, in increments of 1 day (86400 seconds)
    for dayStart in range(1554069600, 1561845600, 86400): # TODO make into 5 min intervals instead of checking every second
        if len(timesList) == 0:
            return 0
        if timesList[0] > dayStart + 86400:
            continue

        dayRange = range(dayStart, dayStart + 86399)

        # CurrentDayEvents = np.intersect1d(dayRange, timesList)
        CurrentDayEvents = getDayEvents(timesList, dayStart)
        if previousDay is None or (len(previousDay) + len(CurrentDayEvents)) == 0:
            previousDay = toTimeSinceMidnight(CurrentDayEvents, dayStart)
            continue

        timeOfDay = toTimeSinceMidnight(CurrentDayEvents, dayStart)

        dice = 2 * len(np.intersect1d(previousDay, timeOfDay)) / (len(previousDay) + len(timeOfDay))
        diceValues.append(dice)
        previousDay = timeOfDay
    
    if len(diceValues) > 0:
        return np.mean(diceValues)
    return 0

def getDiceFromDict(timesDict: dict):
    return {key: getDiceCoefficient(timesList) for key, timesList in timesDict.items()}

def getDiceMean(timesDict: dict):
    return np.mean(timesDict.values())

# in: list of <tuple> (hour, minutes), in 24 hour, 60 min format. Ex. [(23,59), (14,25), (00,45), (12,0)]
# returns list of angles corresponding to these times
def getTimesAngles(times):
    return np.array([((h * 60 + m) / (24 * 60)) * 2 * np.pi for h,m in times])

# Convert times to angles, and use those to determine circular variance
# in: list of <tuple> (hour, minutes), in 24 hour, 60 min format. Ex. [(23,59), (14,25), (00,45), (12,0)]
# returns a single float value representing variance
def getCircularVariance(times):
    angles = getTimesAngles(times)

    # Calculate the mean resultant length
    C = np.mean(np.cos(angles))
    S = np.mean(np.sin(angles))
    R = np.sqrt(C**2 + S**2)

    # Calculate the circular variance
    circular_variance = 1 - R
    return circular_variance