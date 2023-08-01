from agents.flant5 import AgentFlan
from utils import rand_start, rand_end, get_pruned_graph, get_summary, format_options
from templates import templates
from random import shuffle
from collections import Counter

agent = AgentFlan()

graph = get_pruned_graph()
start = rand_start(graph)
end = rand_start(graph)
start = "Basa (fish)"
end = "Animal slaughter"
start, end = ("Bacon soup", "Ostrich meat")

desc = get_summary(end, agent)

curr = start
path = []


def get_ensemble(links, num):
    links = list(links)
    cnt = Counter()

    for i in range(num):
        shuffle(links)
        links_str = format_options(links)

        inputs = templates["general"].format(goal=end, links=links_str,
                                             desc=desc)
        output = agent.raw_prompt(inputs)

        inputs_conf = templates["confidence"].format(goal=end, choice=output,
                                                     desc=desc)
        output_conf = int(agent.raw_prompt(inputs_conf))

        cnt[output] += output_conf

    print(cnt.most_common())

    return cnt.most_common(1)[0][0]


print(f"Start: {start}, Goal: {end}")

for i in range(10):
    path.append(curr)

    output = get_ensemble(graph[curr], 5)

    print('---')
    print(output)
    print('===')

    if output not in graph[curr]:
        print(
            f"Agent responded with a link that doesn't exist on this page: {output}")
        break

    if len(graph[output]) == 0:
        print(
            f"Agent responded with a link that doesn't exist: {output}")
        break

    if output == end:
        path.append(output)
        print("The end has been reached!")
        break

    curr = output

print(path)

# There are three main issues with this technique.
# The first major issue is that the LLM constantly will find itself in a loop. For instance, it will cycle between "Olive Oil" and "List of vegetable oils"
# The second major issue is that the LLM will often respond with a link that doesn't exist on the page
# The third major issue is that the input context length is huge, which can often confuse the LLM

# We will seek for 2 fixes:
# The first solution is the DC method, which will resolve the third issue
# The second solution is a consult method (using 2 LLMs that will talk things out with each other), which aims to resolve the first and second issue
