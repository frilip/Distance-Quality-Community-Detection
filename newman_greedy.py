import networkx as nx
from distance_quality_function import distance_quality, generate_distance_args
import heapq
import numpy as np
#from networkx.utils.mapped_queue import MappedQueue


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


def newman_greedy_distance(G, gamma):
    '''
    expanation
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

        communities = [[node] for node in cc_graph.nodes()]

        current_quality = distance_quality(cc_graph,communities,gamma,degrees,m,shortest_paths_len,diameter, Pr, D_v_expected)

        # array that holds D_Q(i,j) (difference of quality function if I join communities i,j)
        D_Q = np.zeros((cc_graph.number_of_nodes(), cc_graph.number_of_nodes()))
        # max heap containing (only non negative) max values of DQ for every node
        H = MaxHeap()

        for i in range (cc_graph.number_of_nodes()):
            max_dq = 0
            j_of_max_dq = None
            for j in range (cc_graph.number_of_nodes()):
                if (i==j):
                    continue
                # calculate D_Q(i,j)
                D_Q[i][j] = 2 * ( (1 - gamma) * D_v_expected[i][j] - gamma * shortest_paths_len[i][j] )
                # if they are non negative, add them to heap
                if ( D_Q[i][j] > max_dq ):
                    max_dq = D_Q[i][j]
                    j_of_max_dq = j
            if ( j != None ):
                # use -max_dq so heap performs as a max heap
                H.push( (max_dq, i, j_of_max_dq) )

        
        while H.heap: # heap has elements
            Dq, i, j = H.pop()  # max D_Q 
            print(i,j)
            # merge communities i, j into community j
            communities[j] = communities[i] + communities[j]
            communities[i] = []      # remove community i
             
            # update D_Q(i,j)
            # D_Q(j,k) for every k becomes: D_Q(i,k) + D_Q(j,k), same for D_Q(k,j)
            max_dq = 0       # keep track of max DQ
            k_of_max_dq = None
            for k in range (cc_graph.number_of_nodes()):
                if (j==k):
                    continue
                D_Q[j][k] = D_Q[i][k] + D_Q[j][k]
                D_Q[k][j] = D_Q[i][k] + D_Q[j][k]
                # make D_Q(i,.) 'none' so that it is not considered from now on, same for D_Q(.,i)
                D_Q[i][k] = None    
                D_Q[k][i] = None

                if (D_Q[j][k] >= max_dq):
                    max_dq = D_Q[j][k]
                    k_of_max_dq = k

            
            # update heap H: change the value corresponding to node j, to have correct D_Q
            # also update elements where j is the target

            # remove heap items corresponding to j
            for item in H.iterate():
                if item[1] == j:
                    H.remove(item)
                if item[2] == j:
                    H.remove(item)
                    # add max of item[1]th row
                    max_dq_target = 0
                    target = None
                    for k in range (cc_graph.number_of_nodes()):
                        if (D_Q[item[1]][k] > max_dq_target):
                            max_dq_target = D_Q[item[1]][k]
                            target = k
                    if target!=None:
                        H.push( (max_dq_target, item[1], target) )
            # add correct values (only if it is non negative)
            if k_of_max_dq != None:
                H.push( (D_Q[j][k_of_max_dq], j, k_of_max_dq) )
                print("----", j,k_of_max_dq)

        return communities





# ------------- TEST -----------------
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edges_from([(1,2),(1,4),(1,3),(2,4),(2,5),(3,4),(4,5),(5,6)])
newman_greedy_distance(G,0.03)