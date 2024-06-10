import dataAnalysis

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import circmean

def wakeSleepCircle(wakeTimes, sleepTimes, patientId):
    wakeAngles = dataAnalysis.getTimesAngles(wakeTimes)
    sleepAngles = dataAnalysis.getTimesAngles(sleepTimes)

    # plt.plot(np.cos(np.linspace(0, 2*np.pi, 500)),np.sin(np.linspace(0, 2*np.pi, 500)),c='k', zorder=-1)
    # plt.axis('equal')
    # plt.axis('off')

    # print(wakeTimes)

    ax = plt.subplot(111, polar=True, zorder=1)
    # ax.scatter(np.cos(wakeAngles), np.sin(wakeAngles))
    ax.scatter(wakeAngles, np.ones(len(wakeAngles))*0.95, zorder=5, facecolor="r", edgecolor="black")
    ax.scatter(circmean(wakeAngles), np.ones(1)*0.75, zorder=6, facecolor='r', s=250, marker="X", 
            linewidth=1, edgecolor='k')
    ax.scatter(sleepAngles, np.ones(len(sleepAngles))*0.9, zorder=5, facecolor="b", edgecolor="black")
    ax.scatter(circmean(sleepAngles), np.ones(1)*0.75, zorder=6, facecolor='b', s=250, marker="X", 
            linewidth=1, edgecolor='k')
    ax.grid(which='major', axis='y')

    # suppress the radial labels
    plt.setp(ax.get_yticklabels(), visible=False)

    # set the circumference labels
    ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
    ax.set_xticklabels([f'{i:02d}:00' for i in range(24)])
    ax.tick_params(pad=15)

    # make the labels go clockwise
    ax.set_theta_direction(-1)
    ax.legend(['First line', 'Second line', '3', '4'])

    # place 0 at the top
    # ax.set_theta_offset(np.pi/2.0)    

    # plt.grid('off')

    # put the points on the circumference
    plt.ylim(0,1)

    plt.show()

    # plt.scatter(np.cos(wakeAngles), np.sin(wakeAngles), c='b', s=15)
    # plt.scatter(np.cos(circmean(wakeAngles)), np.sin(circmean(wakeAngles)), c='g', s=15)
    # plt.scatter(np.cos(sleepAngles), np.sin(sleepAngles), c='y', s=15)
    # plt.scatter(np.cos(circmean(sleepAngles)), np.sin(circmean(sleepAngles)), c='r', s=15)
    # plt.savefig(f'figures/test1/{patientId} no-nap sleep circle')
    # plt.close()

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

# if __name__ == "__main__":

#     wakeSleepCircle(wakeTimes, sleepTimes, patientId):