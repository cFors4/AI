from time import time
import numpy as np

from sklearn.cluster import KMeans
from sklearn.datasets import load_digits

from scipy.stats import mode
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling

np.random.seed(42)

#time taken to carry out k means processing
t0 = time()
digits = load_digits()
kmeans = KMeans(n_clusters=10, random_state=0)
print ("done in %0.3fs" % (time() - t0))

#plot clusters for each number a visual representation of accuracy
clusters = kmeans.fit_predict(digits.data)
fig, ax = plt.subplots(2, 5, figsize=(8, 3))
centers = kmeans.cluster_centers_.reshape(10, 8, 8)
for axi, center in zip(ax.flat, centers):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)

plt.show()

#plot confusion matric, shows confusion between 8 and 1
labels = np.zeros_like(clusters)
for i in range(10):
    mask = (clusters == i)
    labels[mask] = mode(digits.target[mask])[0]

data = digits.data

mat = confusion_matrix(digits.target, labels)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=digits.target_names,
            yticklabels=digits.target_names)
plt.xlabel('true label')
plt.ylabel('predicted label');

plt.show()

#genearl information
#dataset
n_samples, n_features = data.shape
n_digits = len(np.unique(digits.target))

print ("n_digits: %d" % n_digits)
print ("n_features: %d" % n_features)
print ("n_samples: %d" % n_samples)
#the sum of squared error for each cluster
print ("inertia: %f" % kmeans.inertia_)
#getting accuracy from target data
print("accuracy: ",accuracy_score(digits.target, labels))
