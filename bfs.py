from collections import deque, defaultdict
from utils import rand_start, rand_end, get_pruned_graph


def shortest_dist(start, end):
    explored = set()
    queue = deque()
    queue.append(start)

    parents = defaultdict(str)

    while len(queue) > 0:
        for _ in range(len(queue)):
            curr = queue.popleft()

            if curr == end:
                res = []
                cur_res = end

                while cur_res != "":
                    res.insert(0, cur_res)
                    cur_res = parents[cur_res]

                return res

            if curr in explored:
                continue

            explored.add(curr)

            for node in graph[curr]:
                if node not in explored:
                    queue.append(node)

                    if parents[node] == "":
                        parents[node] = curr

    return []

graph = get_pruned_graph()
start = rand_start(graph)
end = rand_start(graph)
start = "Vegetarianism"
end = "Industrial Revolution"
start, end = ("Bacon soup", "Ostrich meat")
path = shortest_dist(start, end)
path_str = ", ".join(path)

print(
    f"There are {len(path) - 1} links between the Wikipedia pages for {start} and {end}: [{path_str}]")
