import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

def shortest_path(coords):
    lat, lon = coords

    north = -23.511798
    south = -23.519742
    east = -46.180065
    west = -46.189472

    """
    north = -23.511798
    south = -23.519742
    east = -46.180065
    west = -46.189472
    """

    bbox = [west, south, east, north]

    G = ox.graph_from_bbox(bbox, network_type='drive')

    fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")
    plt.show()
    return

    # Find the nearest existing node to connect
    nearest_node = ox.distance.nearest_nodes(G, lon, lat)

    # Generate a unique node ID (or use a custom one)
    new_node_id = max(G.nodes) + 1  # Ensure it's unique

    # Add the new node with its attributes
    G.add_node(new_node_id, x=lon, y=lat)

    print(nearest_node)

    # Add an edge between the new node and the nearest node
    G.add_edge(new_node_id, nearest_node, length=ox.distance.great_circle(
        lat, lon,  # First point coordinates
        G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x']  # Second point coordinates
    ))


    custom_weights = {
        (357130378, 357130374): 50,  
        (357130378, 357213103): 10,
        (357213103, 357213101): 120,
        (357130374, 357213101): 500000000000,
        (357213101, 357213098): 140,
        (357213098, 357213104): 150,
        (357213098, 357213110): 100,
        (357213104, 357213109): 110,
        (357213109, 357213110): 120,
        (357213110, 357213097): 140
    }


    for u, v, data in G.edges(data=True):
        if (u, v) in custom_weights:
            data['weight'] = custom_weights[(u, v)]

    beginning = new_node_id
    ending = [list(G.nodes())[-2]]

    distances, paths = nx.single_source_dijkstra(G, source=beginning, weight='weight')

    shortest_target = min(ending, key=lambda t: distances[t])  
    shortest_path = paths[shortest_target]

    fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")

    for node in G.nodes():
        x, y = G.nodes[node]["x"], G.nodes[node]["y"]
        ax.text(x, y, str(node), fontsize=8, color="black")

    plt.show()
    return 

    #uvicorn endpoint:app --host 0.0.0.0 --port 8000 --reload     plt.show()

    json_path = [
        {"node": node, "lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"]}
        for node in shortest_path
    ]

    return json_path
