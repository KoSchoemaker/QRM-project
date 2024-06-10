import numpy as np
import matplotlib.pyplot as plt

import json

def plotEfficiency():

    with open('intermediate_results/efficiencies.json', 'r') as f:
        dvs = json.load(f)

    with open('intermediate_results/patient_clustering_results_bigger_sample.json', 'r') as f:
        clusters = json.load(f)

    totalSleepTime = [val['totalSleepTime'] for val in list(dvs.values())]
    totalMinutesInBed = [val['totalMinutesInBed'] for val in list(dvs.values())]
    eff = [val['sleepEfficiency'] for val in list(dvs.values())]

    patientIds = list(dvs.keys())

    colorarr = ['blue' if color==0 else 'orange' for color in clusters.values()]

    print(eff)
    arr1inds = np.array(eff).argsort()

    eff = np.array(eff)[arr1inds[::-1]]
    patientIds = np.array(patientIds)[arr1inds[::-1]]
    colorarr = np.array(colorarr)[arr1inds[::-1]]



    # plt.scatter(totalSleepTime, totalMinutesInBed, c=list(clusters.values()))
    # plt.xlabel('Total Sleep Time (seconds)')
    # plt.ylabel('Total Time In Bed (seconds)')
    # # plt.title()
    # plt.show()

    # plt.bar(patientIds, eff)
    # plt.xticks(rotation='vertical')
    # plt.xlabel('Total Sleep Time (seconds)')
    # plt.ylabel('Total Time In Bed (seconds)')

    # fig, ax = plt.subplots()
    ax = plt.subplot(111)

    ax.bar(patientIds, eff, label=patientIds, color=colorarr, zorder=3)

    ax.set_ylabel('Sleep Efficiency')
    ax.set_xlabel('Patient')
    ax.set_title('Sleep Efficiency for each Patient')
    ax.legend(['no routine', 'routine'], title='clusters', loc='upper right')
    leg = ax.get_legend()
    leg.legend_handles[0].set_color('orange')
    leg.legend_handles[1].set_color('blue')
    ax.tick_params(axis='x', labelrotation=90)
    ax.grid(zorder=0, axis='y')
    plt.ylim(0,1)
    # plt.title()
    plt.show()

plotEfficiency()
