import sleepSchedule
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import circmean

def wakeSleepCircle(wakeTimes, sleepTimes, patientId):
    wakeAngles = sleepSchedule.getTimesAngles(wakeTimes)
    sleepAngles = sleepSchedule.getTimesAngles(sleepTimes)

    plt.plot(np.cos(np.linspace(0, 2*np.pi, 500)),np.sin(np.linspace(0, 2*np.pi, 500)),c='k', zorder=-1)
    plt.axis('equal')
    plt.axis('off')
    plt.scatter(np.cos(wakeAngles), np.sin(wakeAngles), c='b', s=15)
    plt.scatter(np.cos(circmean(wakeAngles)), np.sin(circmean(wakeAngles)), c='g', s=15)
    plt.scatter(np.cos(sleepAngles), np.sin(sleepAngles), c='y', s=15)
    plt.scatter(np.cos(circmean(sleepAngles)), np.sin(circmean(sleepAngles)), c='r', s=15)
    plt.savefig(f'{patientId} sleep wake circle')
    plt.close()

def roomUsageCircle(times: dict, patientId):
    pass