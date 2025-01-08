import networkx as nx
from distance_quality_function import distance_quality, generate_distance_args


def greedy_distance_communities(G, gamma, max_iter):
    '''
    Greedy selection implementation of distance quality optimisation
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
        reverse_node_mapping = {new: old for old, new in node_mapping.items()}

        cc_graph = nx.relabel_nodes(cc_graph, node_mapping)

        # generate calculations once
        degrees,m,shortest_paths_len,diameter, Pr, D_v_expected = generate_distance_args(cc_graph)

        communities = [[node] for node in cc_graph.nodes()]

        current_quality = distance_quality(cc_graph,communities,gamma,degrees,m,shortest_paths_len,diameter, Pr, D_v_expected)
        
        times_run = 0
        while times_run < max_iter:  # limit to how many times it can run 
            times_run += 1

            old_quality = current_quality
            # Loop through each node
            for i, community in enumerate(communities):
                for node in community:
                    best_community = None
                    best_delta_quality = 0
                    
                    # Check each other community to see if moving the node improves the distance_quality
                    for j, other_community in enumerate(communities):
                        if i == j:
                            continue
                        
                        # Simulate moving the node to community j
                        new_communities = [c[:] for c in communities]  # Deep copy the communities
                        new_communities[i].remove(node)  # Remove node from its current community
                        new_communities[j].append(node)  # Add node to new community
                        
                        # Calculate the quality of the new partition
                        new_quality = distance_quality(cc_graph,new_communities,gamma,degrees,m,shortest_paths_len,diameter, Pr, D_v_expected)
                        delta_quality = new_quality - current_quality
                        
                        if delta_quality > best_delta_quality:
                            best_delta_quality = delta_quality
                            best_community = j  # The best community to move the node into
                    
                    # Move the node if it improves the quality
                    if best_delta_quality > 0:
                        # Remove node from current community and add it to the best community
                        communities[i].remove(node)
                        communities[best_community].append(node)
            
            # Recalculate the current quality after all node moves
            current_quality = distance_quality(cc_graph,communities,gamma,degrees,m,shortest_paths_len,diameter, Pr, D_v_expected)
            
            # If the quality didn't improve, we stop
            if current_quality <= old_quality:
                break
        
        # reverse node mapping
        reversed_communities = []
        for community in communities:
            reversed_community = [reverse_node_mapping[node] for node in community]
            reversed_communities.append(reversed_community)

        # remove empty communities
        reversed_communities = list(filter(None, reversed_communities))
        # add connected component communities to final communities
        calculated_communities = calculated_communities + reversed_communities

    return calculated_communities
