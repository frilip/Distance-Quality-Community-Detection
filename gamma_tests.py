import networkx as nx
import numpy as np
from jaccard_implementation import jaccard_similarity_communities_optimal
from newman_greedy import newman_greedy_distance
from cluster_graphs import generate_full_cluster_graph_same_size
import matplotlib.pyplot as plt
from color_communites import color_communities

'''
Plot for a variety of graphs the relation of community detection accuracy to gamma values 
'''



cluster_values = np.linspace(3,16,1).astype(int)
cluster_node_values = np.linspace(1,50,30).astype(int)
gamma_values = np.linspace(0.0001,0.1,100)

for clusters in cluster_values:
    for cluster_nodes in cluster_node_values:
        optimal_gamma = None 
        max_accuracy = 0
        for gamma in gamma_values:
            graph = generate_full_cluster_graph_same_size(clusters, cluster_nodes)
            actual_communities = [[k * cluster_nodes + i for i in range(cluster_nodes)] for k in range(clusters)]
            calculated_communities = newman_greedy_distance(graph, gamma)
            accuracy = jaccard_similarity_communities_optimal(actual_communities, calculated_communities)
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                optimal_gamma = gamma
        plt.scatter(cluster_nodes, optimal_gamma, c='red')

        print(cluster_nodes)
plt.show()