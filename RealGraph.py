import networkx as nx
from newman_greedy import newman_greedy_distance_auto, newman_greedy_distance
import csv
from jaccard_implementation import jaccard_similarity_communities_optimal
from networkx.algorithms.community import greedy_modularity_communities


def find_item_in_2d_list(matrix, item):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == item:
                return (i, j)  # Returns the row and column index of the item
    return None  # Returns None if the item is not found




# Read the edge list from the file
G = nx.read_edgelist("./data/email-Eu-core.txt",create_using=nx.DiGraph(), nodetype = int)
# convert to undirected 
G = G.to_undirected()

# import actual communities
community_dict = {}
with open('./data/email-Eu-core-department-labels.txt', 'r') as file:
    for line in file:
        node, community = line.strip().split()
        if community not in community_dict:
            community_dict[community] = []
        community_dict[community].append(int(node))
actual_communities = list(community_dict.values())


# -----------------------------------------------------------------------------

# calculate communities with expected gamma
communities_expected = newman_greedy_distance_auto(G)



# save them in a csv file
# Create and open a CSV file in append mode
with open('./data/calculated_communities_expectedgamma.csv', 'a', newline='') as f:

    # Create a writer object
    writer = csv.writer(f)
    
    # Append a list as a new row
    writer.writerow(['node', 'calculated_community'])
    for node in range (1005):
        comm,j = find_item_in_2d_list(communities_expected, node)
        writer.writerow([str(node), str(comm + 1)])


# --------------------------------------------------------------------------


# calculate communities with gamma 
gamma = 0.000007
communities_fixed = newman_greedy_distance(G,gamma)

# save them
# Create and open a CSV file in append mode
with open('./data/calculated_communities_gamma='+str(gamma)+'.csv', 'a', newline='') as f:
    f.truncate()
    # Create a writer object
    writer = csv.writer(f)
    
    # Append a list as a new row
    writer.writerow(['node', 'calculated_community'])
    for node in range (1005):
        comm,j = find_item_in_2d_list(communities_fixed, node)
        writer.writerow([str(node), str(comm + 1)])



# calculate jaccard similarity to actual communities
accuracy = jaccard_similarity_communities_optimal(actual_communities, communities_fixed)
print('accuracy distance =', accuracy)

# -------------------------------------------------------------------

# calculate communities using modularity 
communities_modularity = greedy_modularity_communities(G)
# convert to list from frozenset
# Step 1: Convert the outer frozenset to a list
outer_list = list(communities_modularity)
# Step 2: Convert each inner frozenset to a list
communities_modularity = [list(inner_set) for inner_set in outer_list]

# save them
# Create and open a CSV file in append mode
with open('./data/calculated_communities_modularity.csv', 'a', newline='') as f:
    f.truncate()
    # Create a writer object
    writer = csv.writer(f)
    
    # Append a list as a new row
    writer.writerow(['node', 'calculated_community'])
    for node in range (1005):
        comm,j = find_item_in_2d_list(communities_modularity, node)
        writer.writerow([str(node), str(comm + 1)])

# calculate jaccard similarity to actual communities
accuracy_modularity = jaccard_similarity_communities_optimal(actual_communities, communities_modularity)
print("accuracy modularity =", accuracy_modularity)