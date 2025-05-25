import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import datetime  
import random  
import os

# DELIMITA OS VÉRTICES DE DESTINO DO GRAFO 
# LOCAIS CONSIDERADOS SEGUROS
safeNodes = [
    {
        "lat":-23.514377, 
        "lon":-46.183998,
        "local":"Terminal Rodoviario",
        "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
        "nodeId":""
    },
    {
        "lat":-23.516449,
        "lon":-46.185012,
        "local":"Terminal Estudantes",
        "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
        "nodeId":""
    },
    {
        "lat":-23.518150, 
        "lon":-46.187190,
        "local":"Polícia Cívil",
        "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
        "nodeId":""
    },
    {
        "lat":-23.519292, 
        "lon":-46.185442,
        "local":"Prédio Prefeitura",
        "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
        "nodeId":""
    },
    {
        "lat":  -23.515693, 
        "lon":-46.187338,
        "local":"Tiro de Guerra",
        "foto":"https://i.ibb.co/DPW33gsd/pinpoint-removebg-preview.png",
        "nodeId":""
    }
]

# FUNÇÃO PARA ADICIONAR NOVO VÉRTICE AO GRAFO
def add_node(lat, lon, G): 
    nearest_node = None

    # ENCONTRA O VÉRTICE MAIS PRÓXIMO A PARTIR DA LATITUDE E LONGITUDE INFORMADA
    nearest_node = ox.distance.nearest_nodes(G, lon, lat)

    # GERA UM ID ÚNICO PARA O VÉRTICE
    new_node_id = max(G.nodes) + 1

    # ADICIONA O VÉRTIDO AO GRAFO
    G.add_node(new_node_id, x=lon, y=lat)

    # OBTÉM A DISTÂNCIA-ARESTA ENTRE O VÉRTICE E O VÉRTICE MAIS PRÓXIMO
    distance = ox.distance.great_circle(
        lat, lon,
        G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x']
    )

    # ADICIONA A ARESTA ENTRE O VÉRTICE E O VÉRTICE MAIS PRÓXIMO
    G.add_edge(new_node_id, nearest_node, length=distance, weight=distance)
    G.add_edge(nearest_node, new_node_id, length=distance, weight=distance)
    
    # RETORNA O GRAFO (G) E O ID DO VÉRTICE ADICIONADO
    return G, new_node_id

# FUNÇÃO PARA DETERMINAR PESOS COM BASE NO HORÁRIO
def get_time_based_weight(is_heavy_traffic=False):
    current_hour = datetime.datetime.now().hour
    
    # PARA DIA: 5:00 ATE 17:00 (5-17)
    if 5 <= current_hour < 17:
        if is_heavy_traffic: # CASO SEJA DE TRAFEGO PESADO, PESO MAIOR
            return random.randint(20, 30)  
        else:
            return random.randint(10, 25) 
    # PARA NOITE: 17:00 ATE 5:00 (17-5)
    else:
        if is_heavy_traffic:
            return random.randint(25, 55) # CASO DE TRAFEGO PESADO, PESO MAIOR
        else:
            return random.randint(19, 35)  

# FUNÇÃO PARA CALCULAR CAMINHO MENOS CUSTOSO
def shortest_path(coords):
    # VETOR PARA ARMAZENAR OS IDs DOS VÉRTICES SEGUROS
    safeNodesIds = []

    # OBTÉM LATITUDE E LONGITUDE PELAS COORDENADAS ENVIADAS
    lat, lon = coords

    # DELIMITA A ÁREA DO MAPA QUE OS VÉRTICES SERÃO EXTRAÍDOS
    # EXTREMOS NORTE, SUL, LESTE E OESTE DO MAPA OPENSTREETMAP
    north = -23.511798
    south = -23.519742
    east = -46.180820
    west = -46.189472

    # UNE EM UMA ARRAY OS PONTOS PARA EXTRAÇÃO DOS VÉRTICES
    bbox = [west, south, east, north]

    # OBTÉM O GRAFO EM UMA REDE DO TIPO ANDAR.
    G = ox.graph_from_bbox(bbox, network_type='walk')
    
    # CRIA O VÉRTICE COM A LOCALIZAÇÃO PASSADA NA FUNÇÃO
    G, new_node_id = add_node(lat, lon, G)

    # ITERA O VERTOR COM OS VÉRTICES SEGUROS, E OS ADICIONA NO GRAFO
    for location in safeNodes:
        G, nodeId = add_node(location["lat"], location["lon"], G)
        location['nodeId'] = nodeId
        safeNodesIds.append(nodeId)
    
    # DETERMINA ARESTAS COM TRÁFEGO PESADO (MOVIMENTADAS)
    heavy_traffic_edges = [
        (356305920, 356305925), (356315514, 356315512),
        (356306090, 356306091), (356306091, 6264967367),
        (6264967367, 356306111), (356306111, 2435125370),
        (356306102, 5661432523), (5661432523, 356306103),
        (356306108, 5755074585), (5661432417, 356351102),
        (5755074565, 5755074574), (5755074562, 5755074571),
        (5755074578, 1819607178), (5755074575, 356306155),
        (3306164150, 3306164142), (3306164142, 7930322009),
        (3306164116, 3306164113), (3306164113, 3306164115),
        (3306164118, 3306164115), (3306164115, 3306164127),
        (356351102, 356351098), (356351102, 356351212),
        (356351208, 356351296), (356351296, 356351120)
    ]
    
    # DELIMITA AS ARESTAS RELEVANTES DO GRAFO
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
    
    # VARIAVEL PARA ARMZENAR PESO DAS ARESTAS
    edge_weights = {}

    # ITERA AS ARESTAS DO VETOR all_connections
    for edge in all_connections:
        edge_key = tuple(sorted(edge))  # OBTEM O ID DA ARESTA
        is_heavy = edge in heavy_traffic_edges or tuple(reversed(edge)) in heavy_traffic_edges # VERIFICA SE É DE ALTO TRÁFEGO
        edge_weights[edge_key] = get_time_based_weight(is_heavy) # ADICIONA PESO A ARESTA

    # ITERA AS ARESTAS PARA ASSOCIAR O PESO
    for u, v, data in G.edges(data=True):
        #  OBTEM O ID DA ARESTA
        edge_key = tuple(sorted([u, v]))

        # VERIFICA SE ARESTA JÁ ESTÁ COM PESO DEFINIDO
        if edge_key in edge_weights:
            weight = edge_weights[edge_key] # ARMAZENA PESO DA ARESTA
        else:
            # VERIFICA SE A ARESTA JÁ RECEBEU VALOR (EVITAR DUPLICAR)
            if edge_key not in edge_weights:
                edge_weights[edge_key] = random.randint(10, 50)
            weight = edge_weights[edge_key] # ARMAZENA PESO DA ARESTA

        # ADICIONA O PESO COMO ATRIBUTO WEIGHT DA ARESTA
        data["weight"] = weight

    # DELIMITA O VÉRTICE DE INÍCIO PARA O DIJKSTRA
    beginning = new_node_id

    # DELIMITA O(S) VÉRTICE(S) DE TÉRMINO PARA O DIJKSTRA
    ending = safeNodesIds

    # OBTEM DISTÂNCIAS E CAMINHOS PARA OS PONTOS DE DESTINO USANDO DIJKSTRA
    distances, paths = nx.single_source_dijkstra(G, source=beginning, weight='weight')

    # ENCONTRA O VÉRTICE DESTINO COM O CAMINHO MENOS CUSTOSO
    shortest_target = min(ending, key=lambda t: distances[t])

    # ARMZENA O CAMINHO MAIS CURTO EM UMA VARIÁVEL
    shortest_path = paths[shortest_target]

    # INICIALIZA A PLOTAGEM DO GRAFO (EXIBIR IMAGEM)
    fig, ax = ox.plot_graph(G, show=False, close=False, node_color="red", node_size=50, edge_linewidth=1, bgcolor="white")

    # DESENHA PESO DAS ARESTAS 
    drawn_edges = set()
    for u, v, data in G.edges(data=True):
        # VERIFICA SE AS ARESTAS POSSUEM PESO
        if 'weight' in data:
            # ARMAZENA ID DO VERTICE 
            edge_key = tuple(sorted([u, v]))
            # VERIFICA SE JÁ FOI DESENHADO, PARA EVITAR DUPLICIDADE
            if edge_key not in drawn_edges:
                drawn_edges.add(edge_key)

                # OBTEM O PONTO INTERMEDIÁRIO ENTRE OS VÉRTICES DA ARESTA PARA DESENHAR O PESO
                x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
                x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                
                # DESENHA O PESO NO INTERMÉDIO DA ARESTA
                ax.text(mid_x, mid_y, f'{data["weight"]:.0f}', fontsize=8, color='black', alpha=0.9, ha='center', va='center')

    # DESENHA O CAMINHO MAIS CURTO NA PLOTAGEM DO GRAFO
    ox.plot_graph_route(G, shortest_path, ax=ax, route_linewidth=4, route_color="yellow", alpha=1)
    
    # OBTÉM O VÉRTICE DE DESTINO
    targetNode = None
    for node in safeNodes:
        if node.get("nodeId") == shortest_target:
            targetNode = node

    # CRIA DOCUMENTO JSON COM TODOS OS VÉRTICES DO CAMINHO MENOS CUSTOSO
    json_path = {
        "path": [
            {"node": node, "lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"]}
        for node in shortest_path
        ],
        "target": targetNode
    }   

    # RETORNA O DOCUMENTO
    return json_path