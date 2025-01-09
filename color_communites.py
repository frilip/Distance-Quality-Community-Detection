import matplotlib.pyplot as plt
import networkx as nx

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

