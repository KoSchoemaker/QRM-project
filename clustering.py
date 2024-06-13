from sklearn.cluster import KMeans, MeanShift
import matplotlib.pyplot as plt
import numpy as np
import json

with open('intermediate_results/room_usage_mean_sleep_schedule_sum.json', 'r') as f:
    data = json.load(f)

x = np.array([x['roomUsageDiceMean'] for x in list(data.values())])
y = np.array([y['sleepScheduleVarianceSum'] for y in list(data.values())])

xy = np.concatenate((x.reshape(-1,1), y.reshape(-1,1)), axis=1)

keys = []
values = []
for key, value in data.items():
    values.append(value)
    keys.append(key)

# values = np.array(list(data.values()))
kmeans = KMeans(n_clusters=3, random_state=1234)
kmeans.fit(xy)

newLabels = np.array([1 if int(label)==0 or int(label)==1 else 0 for label in kmeans.labels_ ])
newColors = ['orange' if int(label)==0 or int(label)==1 else 'blue' for label in kmeans.labels_ ]

# plt.scatter(x, y, c=newColors)
plt.scatter(x[newLabels==1], y[newLabels==1], facecolor="orange", edgecolor="black", label='No routine (7)')
plt.scatter(x[newLabels==0], y[newLabels==0], facecolor="blue", edgecolor="black", label='Routine (10)')
plt.ylabel('Sleep Schedule Variance')
plt.xlabel('Room Usage Dice-Sørensen coefficient')
ax = plt.gca()

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])

plt.title(f'Clustered Participants Based On Sleep Schedule And Room Usage')
plt.savefig(f'figures/clusters', bbox_inches='tight')
plt.close()

patientClusteringDict = {key: int(newLabels[i]) for i, key in enumerate(keys)}

import json
with open('intermediate_results/patient_clustering_results_bigger_sample.json', 'w') as f:
    json.dump(patientClusteringDict, f)