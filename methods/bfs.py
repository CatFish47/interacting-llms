from collections import deque, defaultdict
import time


def bfs(graph, start, end):
    """Finds the shortest path between the start and end in the graph

    An implementation of a breath-first search algorithm to find the shortest
    path between two vertices in the graph.

    Parameters
    ----------
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link
    start : str
        The starting page in the graph
    end : str
        The ending page in the graph

    Returns
    -------
    str, int
        The link that the agent suggests clicking on and the number of times
        the agent was prompted
    """

    start_time = time.time()

    results = {
        "path": [],
        "time": 0,
        "prompts": 0
    }

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

                end_time = time.time()
                results["path"] = res
                results["time"] = end_time - start_time

                return results

            if curr in explored:
                continue

            explored.add(curr)

            for node in graph[curr]:
                if node not in explored:
                    queue.append(node)

                    if parents[node] == "":
                        parents[node] = curr

    end_time = time.time()
    results["time"] = end_time - start_time

    return results
