import numpy as np
from scipy.optimize import linear_sum_assignment

# Function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Function to compute the Jaccard similarity between two community lists with optimal matching
def jaccard_similarity_communities_optimal(list1, list2):
    # Convert each community to a set for proper Jaccard calculation
    list1_sets = [set(community) for community in list1]
    list2_sets = [set(community) for community in list2]
    
    # Create a similarity matrix where entry (i, j) is the Jaccard similarity between community i from list1 and community j from list2
    similarity_matrix = np.zeros((len(list1_sets), len(list2_sets)))
    
    for i, community1 in enumerate(list1_sets):
        for j, community2 in enumerate(list2_sets):
            similarity_matrix[i, j] = jaccard_similarity(community1, community2)
    
    # Use the Hungarian algorithm (linear_sum_assignment) to find the optimal matching
    row_ind, col_ind = linear_sum_assignment(-similarity_matrix)  # Maximize similarity, so negate the matrix
    
    # Calculate the total similarity based on the optimal matching
    total_similarity = similarity_matrix[row_ind, col_ind].sum()
    
    # Return the total similarity
    return total_similarity / len(row_ind)  # Average similarity
