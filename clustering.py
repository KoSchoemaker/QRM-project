from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import json

with open('roomusagemean_results.json', 'r') as f:
    data = json.load(f)

values = np.array(list(data.values()))
kmeans = KMeans(n_clusters=2)
kmeans.fit(values.reshape(-1,1))

x = values
y = [0 for i in values]

plt.scatter(x, y, c=kmeans.labels_)
plt.show() 