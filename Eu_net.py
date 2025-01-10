import networkx as nx

# Read the edge list from the file
G = nx.read_edgelist("./data/email-Eu-core.txt",create_using=nx.DiGraph(), nodetype = int)

print(G)