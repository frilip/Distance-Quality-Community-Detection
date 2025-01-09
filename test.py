import matplotlib.pyplot as plt
import networkx as nx
from  cluster_graphs import generate_full_cluster_graph_same_size

G = generate_full_cluster_graph_same_size(4,5)
nx.draw(G)
plt.savefig("./plots/fullcliustergraph.pdf")