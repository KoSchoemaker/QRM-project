from sklearn.cluster import KMeans, MeanShift
import matplotlib.pyplot as plt
import numpy as np
import json

with open('roomusagemean_sleepmean_results.json', 'r') as f:
    data = json.load(f)

x = np.array([x[0] for x in list(data.values())])
y = np.array([y[1] for y in list(data.values())])

xy = np.concatenate((x.reshape(-1,1), y.reshape(-1,1)), axis=1)

values = np.array(list(data.values()))
kmeans = KMeans(n_clusters=2)
kmeans.fit(xy)
# x = values
# y = [0 for i in values]
# plt.plot([0,0.5], [0,0.5])
plt.scatter(x, y, c=kmeans.labels_)
plt.show()
plt.close()

# X = xy
# mean_shift = MeanShift()
# mean_shift.fit(X)

# plt.scatter(X[:, 0], X[:, 1], c=mean_shift.labels_, cmap='viridis', marker='o')
# # plt.scatter(mean_shift.cluster_centers_[:, 0], mean_shift.cluster_centers_[:, 1], c='red', marker='x', s=200, linewidths=3, label='Cluster Centers')
# plt.title('Mean Shift Clustering')
# plt.legend()
# plt.show()