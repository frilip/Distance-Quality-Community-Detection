import networkx as nx
import numpy as np
from greedy_distance import greedy_distance_communities
from cluster_graphs import generate_full_cluster_graph_same_size
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def color_communities(H, comm):
    node_colors = {}
    
    # Generate a distinct set of colors based on the number of communities
    num_communities = len(comm)
    color_map = plt.get_cmap("tab20", num_communities)  # Updated colormap retrieval
    
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







# ------------- TEST -----------------
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edges_from([(1,2),(1,4),(1,3),(2,4),(2,5),(3,4),(4,5),(5,6)])

#print( distance_quality(G,[[1,4,5,6],[2,3]], 0.5) )


H = nx.Graph()
H.add_nodes_from([1,2,3])
H.add_edges_from([(1,2),(2,3)])

Cl = generate_full_cluster_graph_same_size(4,5)


comm = greedy_distance_communities(Cl, 0.035, 40)

plt.figure()
comm = list(filter(None, comm))
print(comm)
color_communities(Cl, comm)
plt.savefig('./plots/cluster_4,5gamma=0.035,my.pdf')


plt.figure()
Cl = generate_full_cluster_graph_same_size(20,8)


comm = greedy_distance_communities(Cl, 0.01, 100)


comm = list(filter(None, comm))
print(comm)
color_communities(Cl, comm)
plt.savefig('./plots/cluster_20,8,gamma=0.01my.pdf')