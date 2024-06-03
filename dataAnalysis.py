import numpy as np
import datetime

def toTimeSinceMidnight(timestampList):
    if len(timestampList) == 0:
        return []
    # print(timestampList[0])
    dt = datetime.datetime.fromtimestamp(int(timestampList[0]))
    dayStart = datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0).timestamp()

    return [timestamp - dayStart for timestamp in timestampList]

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

def getDiceCoefficient(timesList):
    diceValues = []
    previousDay = None
    lounge = timesList
    for dayStart in range(1554069600, 1561845600, 86400):
        dayRange = range(dayStart, dayStart + 86399)

        loungeCurrentDay = np.intersect1d(dayRange, lounge)
        print(loungeCurrentDay)
        if previousDay is None or (len(previousDay) + len(loungeCurrentDay)) == 0:
            previousDay = toTimeSinceMidnight(loungeCurrentDay)
            continue

        timeOfDay = toTimeSinceMidnight(loungeCurrentDay)

        dice = 2 * len(np.intersect1d(previousDay, timeOfDay)) / (len(previousDay) + len(timeOfDay))
        diceValues.append(dice)
        previousDay = timeOfDay
    
    if len(diceValues) > 0:
        return np.mean(diceValues)
    return 0

def getCircularVarianceFromDict(timesDict: dict):
    return {key: getDiceCoefficient(timesList) for key, timesList in timesDict.items()}

def getVarianceSum(sleepVariance: dict, roomUsageVariance: dict):
    return sum(sleepVariance.values()) + sum(roomUsageVariance.values())

if __name__ == "__main__":
    print(getVarianceSum({1:12, 2:14}, {5:5, 8:7}))