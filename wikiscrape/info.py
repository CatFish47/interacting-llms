import pickle

graph = None

# Read dictionary pkl file
with open('graph.pkl', 'rb') as fp:
    graph = pickle.load(fp)

explored_links = set(graph.keys())
all_links = set()

for key in explored_links:
    all_links = all_links | graph[key]

all_links = all_links | explored_links

print(len(all_links))