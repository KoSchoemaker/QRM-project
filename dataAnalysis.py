import numpy as np

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

def getCircularVarianceFromDict(timesDict: dict):
    return {key: getCircularVariance(timesList) for key, timesList in timesDict}

def getVarianceSum(sleepVariance: dict, roomUsageVariance: dict):
    return sum(sleepVariance.values()) + sum(roomUsageVariance.values())

if __name__ == "__main__":
    print(getVarianceSum({1:12, 2:14}, {5:5, 8:7}))