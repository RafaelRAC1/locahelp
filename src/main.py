import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import datetime  
import random  


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

    # Add edge in both directions
    G.add_edge(new_node_id, nearest_node, length=distance)
    G.add_edge(nearest_node, new_node_id, length=distance)
    
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
            "lat":-23.51500,
            "lon":-46.18585,
            "local":"Tiro de Guerra",
            "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
            "nodeId":""
        },
        {
            "lat":-23.51439,
            "lon":-46.18395,
            "local":"pontoOnibus",
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

    # Original custom weights (commented out)
    """
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
    """

    # Generate time-based weights for all connections
    custom_weights = {}
    
    # All connections from the original dictionary
    all_connections = [
        # Previous connections
        (356305920, 356305925), (356315514, 356315512), (356315512, 356315457),
        (356315457, 356315369), (356315369, 356315526), (356315369, 356306091),
        (356306091, 356496367),
        
        # Connections from Img 1
        (356306090, 356306091), (356306091, 6264967367), (6264967367, 356306116),
        (356306090, 356306147), (356306116, 356306147),
        
        # Connections from Img 2
        (6264967367, 356306111), (356306111, 2435125370), (2435125370, 356306110),
        
        # Connections from Img 3 and 4
        (356306102, 5661432523), (5661432523, 356306103), (5661432523, 356306110),
        (356306110, 356306109), (356306103, 356306109), (356306103, 356306104),
        (356306109, 356306108), (356306108, 356306104), (356306108, 5661432417),
        (356306104, 356306105),
        
        # Previous connections from latest images
        (356306108, 5755074585), (5661432417, 356351102), (356306105, 356351274),
        (356351274, 356351269), (5755074585, 5755074582), (5755074585, 5755074566),
        (5755074582, 5755074570), (5755074566, 5755074570), (5755074566, 5755074565),
        (5755074565, 5755074562), (5755074570, 5755074562), (5661432417, 5755074582),
        
        # New connections from upper part of the map
        (5755074565, 5755074574), (5755074562, 5755074571), (5755074574, 5755074571),
        (5755074574, 5755074578), (5755074578, 5755074575),
        
        # Circle connections
        (5755074578, 1819607178), (5755074575, 356306155), (1819607178, 356306155),
        (1819607178, 12487994438), (12487994438, 3306164155), (3306164155, 3306164150),
        (12487994438, 1819607172), (1819607172, 1819607174), (1819607172, 356306150),
        (356306150, 1725598401), (356306150, 1819607174), (356306155, 356306154),
        (356306154, 1725598401), (1725598401, 1819607155), (356306154, 1819607155),
        
        # Left side connections
        (3306164150, 3306164142), (3306164142, 7930322009), (1819607174, 3306164116),
        
        # Far left connections
        (3306164116, 3306164113), (3306164113, 3306164115), (3306164115, 3306164118),
        (3306164155, 4884161555), (3306164150, 3306164132), (3306164142, 3306164145),
        (7930322010, 3306164127),
        
        # Circle connections on the left
        (3306164118, 3306164115), (3306164115, 3306164127), (3306164127, 3306164145),
        (3306164145, 3306164132), (3306164132, 4884161555),
        
        # Connection back to the beginning
        (3306164113, 356306147),
        
        # Right bottom connections
        (356351102, 356351098), (356351102, 356351212), (356351098, 356351212),
        (356351212, 356351208),
        
        # Upper right connections
        (356351208, 356351296), (356351296, 356351120), (356351120, 356351127),
        (356351127, 4172100710), (4172100710, 4172100714), (356351127, 4172100714),
        (356351296, 356351195), (356351195, 356351193), (356351195, 356351283),
        (356351193, 356351283),
        
        # Connections to upper part of the map
        (356351193, 356351162), (4172100714, 2858472026),
        
        # Connection to previous circle
        (356351283, 1819607155)
    ]
    
    for edge in all_connections:
        is_heavy = edge in heavy_traffic_edges
        custom_weights[edge] = get_time_based_weight(is_heavy)

    for u, v, data in G.edges(data=True):
        if (u, v) in custom_weights:
            data['weight'] = custom_weights[(u, v)]

    beginning = new_node_id
    ending = safeNodesIds

    distances, paths = nx.single_source_dijkstra(G, source=beginning, weight='weight')

    shortest_target = min(ending, key=lambda t: distances[t])  
    shortest_path = paths[shortest_target]

    fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")

    # plt.show()
    
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

    return json_path

