import networkx as nx
import numpy as np
from newman_greedy import newman_greedy_distance
from cluster_graphs import generate_full_cluster_graph_same_size
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from color_communites import color_communities



'''
# ------------- TEST -----------------
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edges_from([(1,2),(1,4),(1,3),(2,4),(2,5),(3,4),(4,5),(5,6)])


H = nx.Graph()
H.add_nodes_from([1,2,3])
H.add_edges_from([(1,2),(2,3)])

clusters, cl_nodes = 4, 5
gamma = 0.02
Cl = generate_full_cluster_graph_same_size(clusters, cl_nodes)


comm = newman_greedy_distance(Cl, gamma)

plt.figure()
print(comm)
print(comm)
color_communities(Cl, comm)
plt.savefig('./plots/cluster_'+str(clusters)+','+str(cl_nodes)+'gamma='+str(gamma)+',newman.pdf')

clusters, cl_nodes = 15, 8
gamma = 0.007
plt.figure()
Cl = generate_full_cluster_graph_same_size(clusters, cl_nodes)


comm = newman_greedy_distance(Cl, gamma)



print(comm)
color_communities(Cl, comm)
plt.savefig('./plots/cluster_'+ str(clusters)+','+str(cl_nodes)+',gamma='+str(gamma)+'newman.pdf')
'''

# test for not connected graph
G1 = generate_full_cluster_graph_same_size(3,4)
G2 = generate_full_cluster_graph_same_size(10,6)
G = nx.disjoint_union(G1, G2)

plt.figure()
comm = newman_greedy_distance(G, 0.01)
print(comm)
color_communities(G, comm)
plt.savefig('./plots/nonconnected.pdf')