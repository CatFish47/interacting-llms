from agents.flant5 import AgentFlan
from utils import rand_start, rand_end, get_pruned_graph, get_summary
from templates import general_template

agent = AgentFlan()

graph = get_pruned_graph()
start = rand_start(graph)
end = rand_start(graph)
start, end = ("Bacon soup", "Ostrich meat")

summary = get_summary(end, agent)

curr = start
path = []

for i in range(10):
    path.append(curr)

    inputs = general_template.format(start=curr, goal=end, path=path,
                                     links=", ".join(graph[curr]), desc=summary)
    output = agent.raw_prompt(inputs)

    print(inputs)
    print(output)
    print('---')

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
