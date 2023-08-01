from collections import deque, defaultdict


def bfs(graph, start, end):
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
