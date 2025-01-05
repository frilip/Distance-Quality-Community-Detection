import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from greedy_distance import greedy_distance_communities
from jaccard_implementation import jaccard_similarity_communities_optimal
import random
from cluster_graphs import generate_full_cluster_graph_same_size



def color_communities(H, comm):
    node_colors = {}
    
    # Generate a distinct set of colors based on the number of communities
    num_communities = len(comm)
    color_map = plt.cm.get_cmap("tab20", num_communities)  # 'tab20' colormap has 20 distinct colors, adjust as needed
    
    # Assign colors to each node based on its community
    for idx, cluster in enumerate(comm):
        for node in cluster:
            node_colors[node] = idx  # Community index

    # Draw the graph with assigned node colors
    pos = nx.spring_layout(H)  # Positions for nodes
    plt.figure(figsize=(8, 8))

    # Map community indices to the colors from the colormap
    community_colors = [color_map(node_colors[node]) for node in H.nodes()]

    # Draw the graph with these colors
    nx.draw(H, pos, with_labels=True, node_size=500,
            node_color=community_colors,
            font_weight='bold', font_size=10)







def benchmark_same_size_clusters(clusters, cluster_nodes, gamma, cutoff, greedy_max_iter):
    '''
    Function that creates same size cluster graphs and randomly replaces edges 
    to test the performance of distance quality function. It uses jaccard similarity 
    to compare calculated communities to the actual ones.
    '''
    
    # make testing graph
    graph = generate_full_cluster_graph_same_size(clusters, cluster_nodes)
    
    actual_communities = [[k * cluster_nodes + i for i in range(cluster_nodes)] for k in range(clusters)]

    # make arrays that will hold jacard similarity values for all iterations for distance and modularity
    similarities_distance = np.zeros(cutoff)
    similarities_modularity = np.zeros(cutoff)
    
    # iterate to remove an intra cluster edge and add an extra cluster randomly
    iterations = 0
    while iterations < cutoff:
        
        # remove random intra cluster edge
        while True:  
            # select random edge in cluster, by selecting first the cluster, then the edge
            # remember, intra cluster nodes are in [k*cluster_nodes,..,(k+1)*cluster_nodes - 1] where k is the cluster
            cluster_selection = random.randint(0, clusters-1)
            node_selection_1 = random.randint(cluster_selection*cluster_nodes, (cluster_selection+1)*cluster_nodes-1)
            node_selection_2 = random.randint(cluster_selection*cluster_nodes, (cluster_selection+1)*cluster_nodes-1)
            if graph.has_edge(node_selection_1, node_selection_2):
                graph.remove_edge(node_selection_1, node_selection_2) # remove
                break

        # add random extra cluster edge
        while True:
            # select two different clusters 
            cluster_selection_1 = random.randint(0, clusters - 1)
            cluster_selection_2 = random.randint(0, clusters - 1)
            if (cluster_selection_1 != cluster_selection_2):
                # select one node from each cluster 
                node_cluster_1 = random.randint(cluster_selection_1*cluster_nodes, (cluster_selection_1+1)*cluster_nodes-1)
                node_cluster_2 = random.randint(cluster_selection_2*cluster_nodes, (cluster_selection_2+1)*cluster_nodes-1)
                if (not graph.has_edge(node_cluster_1, node_cluster_2)):  # selected nodes are not connected
                    graph.add_edge(node_cluster_1, node_cluster_2)
                    break

        # calculate communities with distance quality function
        calculated_communities_distance = greedy_distance_communities(graph, gamma, greedy_max_iter)
        # similarity with actual communities
        similarities_distance[iterations] = jaccard_similarity_communities_optimal(actual_communities, calculated_communities_distance)

        # calculate communities with modularity
        calculated_communities_modularity = nx.algorithms.community.modularity_max.greedy_modularity_communities(graph)
        # similarity with actual communities
        similarities_modularity[iterations] = jaccard_similarity_communities_optimal(actual_communities, calculated_communities_modularity)

        '''
        if (iterations==1 or iterations==3 or iterations==6 or iterations==15):
            plt.figure()
            color_communities(graph, calculated_communities_distance)
            plt.savefig('./plots/iterations='+str(iterations)+'.pdf')'''
        

        iterations += 1

    return similarities_distance, similarities_modularity
    

cutoff = 20
# average jaccard similarities
distance_bench = np.zeros(cutoff)
modularity_bench = np.zeros(cutoff)

times = 100

for i in range(times):    
    similarities_distance, similarities_modularity = benchmark_same_size_clusters(4, 5, 0.035, cutoff, 40)
    distance_bench = distance_bench + similarities_distance
    modularity_bench = modularity_bench + similarities_modularity
# normalise 
distance_bench = distance_bench / times
modularity_bench = modularity_bench / times


plt.plot(distance_bench, label='distance')
plt.plot(modularity_bench, label='modularity')
plt.ylim(bottom=0)
plt.legend()
plt.title('Distace and modularity benchmark')
plt.savefig('./plots/benchmark.pdf')