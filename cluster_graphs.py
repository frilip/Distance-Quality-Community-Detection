import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from greedy_distance import greedy_distance_communities
from jaccard_implementation import jaccard_similarity_communities_optimal
import random


def generate_full_cluster_graph_old(clusters, cluster_nodes):
    '''Generates a graph of 'cluster' in number full graphs, each one of those
    has 'cluster_nodes' in number nodes'''

    G = nx.complete_graph(cluster_nodes)

    for i in range (clusters - 1):
        # generate cluster
        full_graph = nx.complete_graph(cluster_nodes) 
        
        last_G_node = list(G.nodes)[-1]
        # combine it with main graph 
        G = nx.disjoint_union(G, full_graph)
        # connect them
        G.add_edge(last_G_node, last_G_node + 1)

    # connect the last and first clusters 
    G.add_edge(list(G.nodes)[0], list(G.nodes)[-1])
    return G


def generate_full_cluster_graph_same_size(clusters, cluster_nodes):
    '''
    Generates a graph of 'cluster' in number full graphs, each one of those
    has 'cluster_nodes' in number nodes and they are connected in a circle.
    
    The clusters have node names in [k*cluster_nodes,.., (k+1)*cluster_nodes - 1]
    with k in [0,..,clusters-1]
    '''

    G = nx.Graph()
    nodes = np.arange(0,clusters*cluster_nodes)
    G.add_nodes_from(nodes)

    # make full clusters
    for k in range(clusters):
        for i in range(cluster_nodes):
            for j in range(i+1, cluster_nodes):
                G.add_edge(k*cluster_nodes + i, k*cluster_nodes + j)
    # connect clusters
    for k in range(clusters-1):
        G.add_edge(k*cluster_nodes + cluster_nodes - 1, k*cluster_nodes + cluster_nodes)
    # connect last and first 
    G.add_edge(0, clusters*cluster_nodes-1)

    return G
