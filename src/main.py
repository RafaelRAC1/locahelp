import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import datetime  
import random  
import os
os.makedirs("algorithms", exist_ok=True)


def add_node(lat, lon, G): 
    nodes = list(G.nodes(data=True))
    nearest_node = None
    min_dist = float('inf')
    # Find the nearest existing node to connect
    nearest_node = ox.distance.nearest_nodes(G, lon, lat)

    # Generate a unique node ID (or use a custom one)
    new_node_id = max(G.nodes) + 1  # Ensure it's unique

    # Add the new node with its attributes
    G.add_node(new_node_id, x=lon, y=lat)

    print(nearest_node)

    # Add an edge between the new node and the nearest node
    distance = ox.distance.great_circle(
        lat, lon,
        G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x']
    )

    # Add edge in both directions with the same weight
    G.add_edge(new_node_id, nearest_node, length=distance, weight=distance)
    G.add_edge(nearest_node, new_node_id, length=distance, weight=distance)
    
    return G, new_node_id

def shortest_path(coords):
    lat, lon = coords

    # Original coordinates (commented out)
    """
    north = -23.54449680628284
    south = -23.546631931890012
    east = -46.2385738438777
    west = -46.24104702097161
    """

    # New coordinates
    north = -23.511798
    south = -23.519742
    east = -46.180820
    west = -46.189472

    bbox = [west, south, east, north]

    # Get the graph without projecting
    G = ox.graph_from_bbox(bbox, network_type='walk')
    
    # Add starting point node
    G, new_node_id = add_node(lat, lon, G)

    # List of safe points coordinates

    # Add safe point
    safeNodes = [
        {
            "lat":-23.51439,
            "lon":-46.18395,
            "local":"Ponto de Onibus",
            "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
            "nodeId":""
        }
    ]

    safeNodesIds = []

    for location in safeNodes:
        G, nodeId = add_node(location["lat"], location["lon"], G)
        location['nodeId'] = nodeId
        safeNodesIds.append(nodeId)
    
    # Function to determine if it's morning or evening and set weights accordingly
    def get_time_based_weight(is_heavy_traffic=False):
        current_hour = datetime.datetime.now().hour
        
        # Morning: 5 AM to 5 PM (5-17)
        if 5 <= current_hour < 17:
            if is_heavy_traffic:
                return random.randint(20, 30)  # Heavy traffic areas in morning
            else:
                return random.randint(10, 25)  # Normal traffic in morning
        # Evening: 5 PM to 5 AM (17-5)
        else:
            if is_heavy_traffic:
                return random.randint(25, 55)  # Heavy traffic areas in evening
            else:
                return random.randint(19, 35)  # Normal traffic in evening
    
    # Define heavy traffic edges (at least 2 from each section)
    heavy_traffic_edges = [
        # Previous connections
        (356305920, 356305925), (356315514, 356315512),
        
        # Connections from Img 1
        (356306090, 356306091), (356306091, 6264967367),
        
        # Connections from Img 2
        (6264967367, 356306111), (356306111, 2435125370),
        
        # Connections from Img 3 and 4
        (356306102, 5661432523), (5661432523, 356306103),
        
        # Previous connections from latest images
        (356306108, 5755074585), (5661432417, 356351102),
        
        # New connections from upper part of the map
        (5755074565, 5755074574), (5755074562, 5755074571),
        
        # Circle connections
        (5755074578, 1819607178), (5755074575, 356306155),
        
        # Left side connections
        (3306164150, 3306164142), (3306164142, 7930322009),
        
        # Far left connections
        (3306164116, 3306164113), (3306164113, 3306164115),
        
        # Circle connections on the left
        (3306164118, 3306164115), (3306164115, 3306164127),
        
        # Right bottom connections
        (356351102, 356351098), (356351102, 356351212),
        
        # Upper right connections
        (356351208, 356351296), (356351296, 356351120)
    ]

    # Generate time-based weights for all connections
    custom_weights = {}
    
    # All connections from the original dictionary
    all_connections = [
        (4561764463, 4561764462), (4561764462, 7927338847), (7927338847, 3560305834), 
        (3560305834, 1791040184), (3560305834, 356306125), (356306125, 356306123), 
        (356306125, 356306139), (356306125, 356306142), (7927338847, 7927338846), 
        (7927338846, 3560305832), (3560305832, 356305951), (356305951, 3560305834), 
        (356306125, 6267878887), (356305951, 356305823), (6267878887, 1791040083), 
        (1791040083, 6267874483), (6267874483, 1791040075), (6267874483, 1791040189), 
        (1791040189, 1723059613), (1723059613, 4138915091), (1791040083, 17191040081), 
        (17191040081, 1791040187), (4138915091, 1791040107), (1791040187, 1791040176), 
        (1791040176, 7930579113), (7930579113, 7930579105), (7930579102, 7930579105), 
        (7930579101, 7930579102), (7930579102, 7930579103), (7930579104, 7930579103), 
        (5844247291, 7930579104), (1791040083, 5844247291), (5844247291, 6267878887), 
        (6267878887, 7931362707), (7931362707, 356306125), (5654900058, 11500782433), 
        (11500782433, 356351156), (356351156, 356614952), (356614952, 356351144), 
        (356351144, 356351141), (356351141, 2858472026), (356351156, 7927560290), 
        (7927560290, 7927560291), (7927560290, 1723059626), (1723059626, 5644743047), 
        (1723059626, 5644743051), (5644743047, 1905915655), (1905915655, 356351170), 
        (5644743051, 356351170), (356351170, 1791040175), (1905915655, 1791040238), 
        (1791040238, 11751676761), (11751676761, 3306166841), (3306166841, 5644743034), 
        (5644743034, 3306166844), (3306166841, 5644743035), (5644743034, 5644743035), 
        (5644743035, 3306166843), (3306166843, 1791040119), (3306166844, 1791040119), 
        (3306166844, 3306166843)
    ]
    
    # Create a dictionary of weights using sorted tuples as keys to ensure consistency
    edge_weights = {}
    for edge in all_connections:
        edge_key = tuple(sorted(edge))  # Use sorted tuple as key
        is_heavy = edge in heavy_traffic_edges or tuple(reversed(edge)) in heavy_traffic_edges
        edge_weights[edge_key] = get_time_based_weight(is_heavy)

    # Assign weights to all edges, ensuring bidirectional consistency
    for u, v, data in G.edges(data=True):
        # Use sorted tuple so (u, v) and (v, u) are treated the same
        edge_key = tuple(sorted([u, v]))

        if edge_key in edge_weights:
            weight = edge_weights[edge_key]
        else:
            # Check if we already assigned a weight to this edge pair
            if edge_key not in edge_weights:
                edge_weights[edge_key] = random.randint(10, 50)
            weight = edge_weights[edge_key]

        data["weight"] = weight

    beginning = new_node_id
    ending = safeNodesIds

    distances, paths = nx.single_source_dijkstra(G, source=beginning, weight='weight')

    shortest_target = min(ending, key=lambda t: distances[t])  
    shortest_path = paths[shortest_target]

    # Plot shortest path
    fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")
    
    route_edges = list(zip(shortest_path[:-1], shortest_path[1:]))

    # Draw edge weights as labels - only once per edge pair
    drawn_edges = set()
    for u, v, data in G.edges(data=True):
        if 'weight' in data:
            # Use sorted tuple to avoid drawing the same edge twice
            edge_key = tuple(sorted([u, v]))
            if edge_key not in drawn_edges:
                drawn_edges.add(edge_key)
                
                # Get midpoint for text placement
                x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
                x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                
                # Plot the weight
                ax.text(mid_x, mid_y, f'{data["weight"]:.0f}', fontsize=8, color='black', alpha=0.9, ha='center', va='center')

    ox.plot_graph_route(G, shortest_path, ax=ax, route_linewidth=4, route_color="yellow", alpha=1)

    # Save figure
    algorithms_folder = "algorithms"
    if not os.path.exists(algorithms_folder):
        os.makedirs(algorithms_folder)

    ## fig.savefig(os.path.join(algorithms_folder, "shortest_path_plot.png"), dpi=300)
    
    for node in G.nodes():
        x, y = G.nodes[node]["x"], G.nodes[node]["y"]
        ax.text(x, y, str(node), fontsize=8, color="black")

    targetNode = None
    for node in safeNodes:
        if node.get("nodeId") == shortest_target:
            targetNode = node

    json_path = {
        "path": [
            {"node": node, "lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"]}
        for node in shortest_path
        ],
        "target": targetNode
    }   

    print(json_path)

    return json_path