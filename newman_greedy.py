import networkx as nx
from distance_quality_function import distance_quality, generate_distance_args
import heapq
import numpy as np
#from networkx.utils.mapped_queue import MappedQueue

'''
class Item:
    def __init__(self, value, data):
        self.value = value
        self.data = data

    def __lt__(self, other):
        return self.value < other.value



class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0]

    def iterate(self):
        for item in self.heap:
            yield (-item[0],) + item[1:]

    def remove(self, value_to_remove):
        for i, item in enumerate(self.heap):
            if item[1] == value_to_remove:
                del self.heap[i]
                heapq.heapify(self.heap)
                return
'''

def newman_greedy_distance(G, gamma):
    '''
    Greedy optimisation using newmans algorithm reference: #addreference
    Starts with every node in its own community and repeatedly merges two communities 
    that have the max change in Q_d if that change is non negative. 
    We only calculate the change in Q_d as its cheaper.
    '''

    # Seperate the graph to its connected components, 
    # Two different connected components should not be in the same community
    components = list(nx.connected_components(G))
    
    calculated_communities = [] # array that will hold communities

    for comp in components:
        # generate induced graph of the component
        cc_graph = G.subgraph(comp)

        # rename the nodes of the graph so that they can work as indices on an array 
        # this will make calling the dynamicly computed information faster to pull
        node_mapping = {old: new for new, old in enumerate(cc_graph.nodes)}
        cc_graph = nx.relabel_nodes(cc_graph, node_mapping)

        # generate calculations once
        degrees,m,shortest_paths_len,diameter, Pr, D_v_expected = generate_distance_args(cc_graph)

        No_comm = cc_graph.number_of_nodes() # number of communities
        communities = [[node] for node in cc_graph.nodes()]

        #current_quality = distance_quality(cc_graph,communities,gamma,degrees,m,shortest_paths_len,diameter, Pr, D_v_expected)


        # initialise matrix that will hold the values of D_Q(i,j) for communities i,j if they are merged
        D_Q = np.empty((No_comm, No_comm))
        # populate it, initial D_Q(i,j) are given by: 2*[(1-gamma)D_V_exp(i,j) - gamma(D_v(i,j)]
        for i in range (No_comm):
            for j in range (No_comm):
                if i==j:
                    D_Q[i][j] = -1 # arbitrary negative value, so that joining the same community is not acounted
                    continue
                D_Q[i][j] = 2 * ( (1-gamma) * D_v_expected[i][j] - gamma * shortest_paths_len[i][j] )

        # communities that result in max DQ
        max_i, max_j = np.unravel_index(np.argmax(D_Q), D_Q.shape)

        while D_Q[max_i][max_j] >= 0:   # while Q can rise 
            # join communities max_i, max_j into max_j
            communities[max_j] = communities[max_j] + communities[max_i]
            communities[max_i] = [] 
            # update D_Q matrix 
            for k in range (No_comm):
                D_Q[max_j][k] = D_Q[max_i][k] + D_Q[max_j][k]
                D_Q[k][max_j] = D_Q[max_i][k] + D_Q[k][max_j]
                D_Q[max_i][k] = -1  # arbitrary negative value
                D_Q[k][max_i] = -1
            # calculate new max indices
            max_i, max_j = np.unravel_index(np.argmax(D_Q), D_Q.shape)

        # add connected component communities to final communities
        calculated_communities = calculated_communities + communities
    return calculated_communities