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

    # print(eff)
    arr1inds = np.array(eff).argsort()

    eff = np.array(eff)[arr1inds[::-1]]
    patientIds = np.array(patientIds)[arr1inds[::-1]]
    colorarr = np.array(colorarr)[arr1inds[::-1]]

    ax = plt.subplot(111)

    ax.bar(patientIds, eff, label=patientIds, color=colorarr, zorder=3, edgecolor='k')

    ax.set_ylabel('Sleep Efficiency')
    ax.set_xlabel('Patient')
    ax.set_title('Sleep Efficiency For Each Patient')
    ax.legend(['Routine (10)', 'No routine (7)'], title='Routine clusters', loc='upper right')
    leg = ax.get_legend()
    leg.legend_handles[0].set_color('blue')
    leg.legend_handles[0].set_edgecolor('k')
    leg.legend_handles[1].set_color('orange')
    leg.legend_handles[1].set_edgecolor('k')
    ax.tick_params(axis='x', labelrotation=90)
    ax.grid(zorder=0, axis='y')
    plt.ylim(0,1)

    plt.savefig(f'figures/efficiencies', bbox_inches='tight')
    plt.close()

def plotRoomUsageExample():
    ax = plt.subplot(111)
    ax.broken_barh([(11.8,1.5),], (38, 9), facecolors='tab:blue', zorder=3)
    ax.broken_barh([(11.8,0.4), (12.4,0.5)], (34, 2), facecolors='tab:green', zorder=3)
    ax.broken_barh([(11.4,0.8), (12.4, 0.5)], (23.5, 9), facecolors='tab:blue', zorder=3)
    ax.broken_barh([(11.4,0.1), (12.6,0.3)], (20, 2), facecolors='tab:green', zorder=3)
    ax.broken_barh([(12.6,0.8), (11.1,0.4)], (10, 9), facecolors='tab:blue', zorder=3)

    ax.set_xlim(11, 14)
    
    ax.set_xlabel('seconds since start')
    ax.set_yticks([15, 21, 28, 35, 43], labels=['day 3', 'overlap', 'day 2', 'overlap', 'day 1'])
    ax.grid(zorder=0)
    
    plt.tight_layout()
    plt.xticks(rotation=45)

    textstr = f'Overlap=1440+1800=3240\nDSC=(2*3240)/(5400+4680)\n=0.64'
    plt.text(12.95, 32.5, textstr, fontsize=9)

    textstr = f'Overlap=360+1080=1440\nDSC=(2*1440)/(4680+4320)\n=0.32'
    plt.text(12.95, 20.5, textstr, fontsize=9)

    plt.text(11.85, 34.5, '1440', fontsize=9)
    plt.text(11.85, 42.5, '5400', fontsize=9)
    plt.text(12.45, 34.5, '1800', fontsize=9)
    plt.text(11.45, 27.5, '2880', fontsize=9)
    plt.text(12.45, 27.5, '1800', fontsize=9)
    plt.text(11.55, 20.5, '360', fontsize=9)
    plt.text(12.65, 20.5, '1080', fontsize=9)
    plt.text(12.65, 14.5, '2880', fontsize=9)
    plt.text(11.15, 14.5, '1440', fontsize=9)

    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x):02d}:{int((x*60)%60):02d}'))
    # ax.xaxis.set_major_locator(plt.MaxNLocator(4))  # Ensure a reasonable number of ticks

    plt.savefig(f'figures/roomUsageExample', bbox_inches='tight')
    plt.close()

plotEfficiency()
plotRoomUsageExample()