from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
import csv
import numpy as np
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

data_type  = 'source'
label_list = []
data = []
with open('./analysis/baseline/baseline_'+data_type+'.csv', mode='r', encoding='utf8') as fp:
    reader = csv.reader(fp)
    header = next(reader)
    for row in reader:
        label_list.append(row[0])
        data.append([float(x.strip()) for x in row[1:]])
analyzer = AgglomerativeClustering(n_clusters=2, compute_distances=True)
cluster_result = dict()
clusters = analyzer.fit(data)
labels = clusters.labels_
for i, label in enumerate(labels.tolist()):
    if label not in cluster_result:
        cluster_result[label] = list()
    cluster_result[label].append(label_list[i])
plt.title('Baseline')
plot_dendrogram(analyzer, orientation='right',
                labels=label_list)
plt_file = './analysis/baseline/baseline_'+data_type+'.png'
plt.savefig(plt_file, bbox_inches='tight')
plt.close()


