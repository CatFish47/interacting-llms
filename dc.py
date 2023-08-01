from agents.flant5 import AgentFlan
from utils import rand_start, rand_end, get_graph, get_summary
from math import ceil
from templates import general_template

agent = AgentFlan()

graph = get_graph()
start = rand_start(graph)
end = rand_end(graph)
# start = "Vegetarianism"
# end = "Charcuterie"
start, end = ("Bacon soup", "Ostrich meat")

desc = get_summary(end, agent)

print(desc)
print('===')

curr = start
path = []


def decide(links, max_per):
    pool = list(links)

    while len(pool) > 1:
        new_pool = []

        path_str = ", ".join(path)

        for i in range(ceil(len(pool) / max_per)):
            mini_pool = pool[i * max_per: min((i + 1) * max_per, len(pool))]

            link_str = ", ".join(mini_pool)

            inputs = general_template.format(goal=end, path=path_str,
                                             links=link_str, desc=desc)
            output = agent.raw_prompt(inputs)

            if output not in mini_pool or len(graph[output]) == 0:
                continue

            new_pool.append(output)

        pool = new_pool
        print(pool)
        print("---")

    if len(pool) == 0:
        print("Decision failed. Pool size reached 0.")
        return ""

    return pool[0]


print(f"Start: {start}, Goal: {end}")

for i in range(10):
    path.append(curr)

    output = decide(graph[curr], 10)
    print("===")

    if output == "":
        break

    if output == end:
        path.append(end)
        break

    curr = output

print(path)
