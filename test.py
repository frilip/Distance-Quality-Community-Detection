import matplotlib.pyplot as plt
import networkx as nx
from  cluster_graphs import generate_full_cluster_graph_same_size
from scipy.optimize import curve_fit
import numpy as np
from newman_greedy import newman_greedy_distance
from jaccard_implementation import jaccard_similarity_communities_optimal

cluster_values = np.linspace(3,10,12).astype(int)
cluster_node_values = np.linspace(4,12,14).astype(int)
gamma_values = np.linspace(0.00001,0.1,100)

data_points = np.empty((0, 2))

for clusters in cluster_values:
    for i, cluster_nodes in enumerate(cluster_node_values):
        optimal_gamma = None 
        max_accuracy = 0
        graph = generate_full_cluster_graph_same_size(clusters, cluster_nodes)
        actual_communities = [[k * cluster_nodes + i for i in range(cluster_nodes)] for k in range(clusters)]
        for gamma in gamma_values:
            calculated_communities = newman_greedy_distance(graph, gamma)
            accuracy = jaccard_similarity_communities_optimal(actual_communities, calculated_communities)
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                optimal_gamma = gamma

        # we have found optimal gamma for clusters and cluster_nodes
        # Append the data to the array
        data_points = np.vstack([data_points, [graph.number_of_edges(), optimal_gamma]])




# Convert data_points to a NumPy array if it's a list of tuples
data_points = np.array(data_points)


# Extract the two variables
x_data = data_points[:, 0]  # The edges (x-values)
y_data = data_points[:, 1]  # The optimal_gamma (y-values)


sorted_indices = np.argsort(x_data)
x_data = x_data[sorted_indices]
y_data = y_data[sorted_indices]



def model(x,c,l):
    return c*np.exp(-l*x)

params, covariance = curve_fit(model, x_data, y_data, p0=[1,1])
c_opt, l_opt = params
print(c_opt, l_opt)

plt.scatter(x_data, y_data, c='red')
x = np.linspace(0,200,100)
plt.plot(c_opt*np.exp(-l_opt * x))