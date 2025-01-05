import networkx as nx
import numpy as np


def distance_quality(G, communities, gamma, degrees, m, shortest_paths_len, diameter, Pr, D_v_expected ):

    ''' 
    This is the function that calculates the distance quality function for the given community,
    to save calculations, everything that is the same between communities is calculated dynamicaly 
    and stored in the function that calls this one. This function takes them as input. 

    This function should not be called on its own, as no tests for the format of the inputs 
    has been implemented!
    '''

    # quality function initialisation
    Q = 0

    for C in communities:
        
        # ---------- Actuall Distance Matrix -----------

        # D_v(C) is the sum of shortest path lengths between every pair in the community
        D_v_C_Actuall = 0
        for node_i in C:
            for node_j in C:
                D_v_C_Actuall += shortest_paths_len[node_i][node_j]
        



        # --------- Expected Distance Matrix -----------

        # initialise sum of expected pairwise distances in cluster C
        D_v_c_expected = 0
        # iterate over community
        for node_i in C:
            for node_j in C:
                # D_v_C_expected is symmetric, diagonal values are added once, while the others are added twice
                if node_i == node_j:
                    D_v_c_expected +=  D_v_expected[node_i][node_j]
                else:
                    D_v_c_expected += 2 * D_v_expected[node_i][node_j]


        # add result to the quality function
        Q += ( (1 - gamma) * D_v_c_expected ) -  ( gamma * D_v_C_Actuall)    # maybe include a gamma ratio

    return Q
        

def generate_distance_args(G):
    '''
    Function that generates once the needed calculations for distance wuality optimisation
    to work. 
    '''


    # Calculate diameter of the subgraph
    diameter = nx.diameter(G) 


    # initialise numpy array that will hold the degrees d_k(i)
    degrees = np.zeros((G.number_of_nodes(), diameter))
    # initialize list that will hold the total number of shortest paths of length k
    # i.e. m_k 
    m = np.zeros(diameter)

    # generate all shortest paths from all nodes 
    for source in G.nodes():
        paths = dict(nx.single_source_shortest_path_length(G, source)) # every shortest path length

        for target, k in paths.items():
            if k > 0: # dont count paths of length 0
                # add 1 to the corresponding degree

                degrees[source][k-1] += 1
                m[k-1] += 0.5 # adding 0.5 because because m = 0.5 * sum of degrees

    # Compute the shortest path lengths between all pairs of nodes in graph
    shortest_paths_len = dict(nx.all_pairs_shortest_path_length(G))

    # initialise array that will hold the probabilities that nodes i,j are connected with a graph of length k
    Pr = np.zeros((G.number_of_nodes(), G.number_of_nodes(), diameter))
    # initialise array that will hold expected distance between i,j
    D_v_expected = np.zeros((G.number_of_nodes(), G.number_of_nodes()))
    for node_i in G:
        for node_j in G:
            for k in range (1,diameter+1):
                
                #calculate probability that vertices i , j are joined by a path of length k
                Pr[node_i][node_j][k-1] = degrees[node_i][k-1] * degrees[node_j][k-1] / (4 * (m[k-1])**2)
                # add it with factor k to expected distance between vertices i , j
                D_v_expected[node_i][node_j] += k * Pr[node_i][node_j][k-1]

    return degrees, m, shortest_paths_len, diameter, Pr, D_v_expected