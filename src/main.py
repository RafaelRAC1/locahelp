import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import json
import os

north = -23.54449680628284
south = -23.546631931890012
east = -46.2385738438777
west = -46.24104702097161

"""
north = -23.51012936142671
south = -23.547848530013358
east = -46.16788873440002
west = -46.22339109326331
"""

bbox = [west, south, east, north]

G = ox.graph_from_bbox(bbox, network_type='drive')

custom_weights = {
    (357130378, 357130374): 50,  
    (357130378, 357213103): 30,
    (357213103, 357213101): 120,
    (357130374, 357213101): 1300,
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

begining = list(G.nodes())[0]  
ending = list(G.nodes())[-1] 

caminho = nx.shortest_path(G, source=begining, target=ending, weight='weight')

fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")

for node in G.nodes():
    x, y = G.nodes[node]["x"], G.nodes[node]["y"]
    ax.text(x, y, str(node), fontsize=8, color="black")

plt.show()

json_path = [
    {"node": node, "lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"]}
    for node in caminho
]

file_path = os.path.join("./src/algorithms/", "dijkstra.json")
with open(file_path, "w") as f:
    json.dump(json_path, f, indent=4)
