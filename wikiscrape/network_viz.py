from pyvis.network import Network
import pandas as pd

import pickle

print("Loading graph...")

graph = None

# Read dictionary pkl file
with open('graph.pkl', 'rb') as fp:
    graph = pickle.load(fp)

print("Graph loaded. Processing Graph...")

explored_links = set(graph.keys())
all_links = set()

for src in graph.keys():
    ns = set()
    for dst in graph[src]:
        if dst in explored_links:
            ns.add(dst)

    graph[src] = ns

for key in explored_links:
    all_links = all_links | graph[key]

all_links = all_links | explored_links
all_links = list(all_links)

print("Graph processed. Generating graph...")

got_net = Network(height="750px", width="100%",
                  bgcolor="#222222", font_color="white", directed=True)

# set the physics layout of the network
got_net.barnes_hut()

print("Adding nodes...")

for n in all_links:
    got_net.add_node(n, title=n)

print("Nodes added. Adding edges...")

edge_data = []

for src in graph.keys():
    for dst in graph[src]:
        edge_data.append((src, dst))

got_net.add_edges(edge_data[0::10])

print("Edges added. Generating HTML...")

# neighbor_map = got_net.get_adj_list()

# # add neighbor data to node hover data
# for node in got_net.nodes:
#     node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
#     node["value"] = len(neighbor_map[node["id"]])

got_net.show("nx.html")

print("Generated HTML.")