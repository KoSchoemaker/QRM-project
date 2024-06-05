import dataAnalysis

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import circmean

def wakeSleepCircle(wakeTimes, sleepTimes, patientId):
    wakeAngles = dataAnalysis.getTimesAngles(wakeTimes)
    sleepAngles = dataAnalysis.getTimesAngles(sleepTimes)

    plt.plot(np.cos(np.linspace(0, 2*np.pi, 500)),np.sin(np.linspace(0, 2*np.pi, 500)),c='k', zorder=-1)
    plt.axis('equal')
    plt.axis('off')
    plt.scatter(np.cos(wakeAngles), np.sin(wakeAngles), c='b', s=15)
    plt.scatter(np.cos(circmean(wakeAngles)), np.sin(circmean(wakeAngles)), c='g', s=15)
    plt.scatter(np.cos(sleepAngles), np.sin(sleepAngles), c='y', s=15)
    plt.scatter(np.cos(circmean(sleepAngles)), np.sin(circmean(sleepAngles)), c='r', s=15)
    plt.savefig(f'{patientId} sleep wake circle')
    plt.close()

def roomUsageBinaryDay(roomsDict, patientId):
    #first date 2019-04-01 00.00.00     1554069600      86400 seconds in a day
    # last date 2019-06-30 23.59.59     1561845600

    lounge = roomsDict['Lounge']

    for dayStart in range(1554069600, 1561845600, 86400):
        dayRange = range(dayStart, dayStart + 86399)

        loungeMask = np.isin(dayRange, lounge)

        plt.plot(dayRange, loungeMask, 'r')
        plt.savefig(f'{patientId} on day {dayStart}')
        plt.close()

def dicePlot(diceValues, patientId):
    plt.ylim(0,1)
    plt.plot(range(len(diceValues)), diceValues, 'r')
    plt.savefig(f'{patientId} diceplot')
    plt.close()

def latencyplot(latencies):
    # plt.ylim(0,1)
    plt.plot(range(len(latencies)), latencies, 'r')
    plt.show()

