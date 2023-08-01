from agents.flant5 import AgentFlan
from utils import rand_start, rand_end, get_pruned_graph, get_summary, format_options
from templates import templates

agent = AgentFlan()

graph = get_pruned_graph()
start = rand_start(graph)
end = rand_start(graph)
# start = "Olive oil"
# end = "Bacon"
start, end = ("Bacon soup", "Ostrich meat")

desc = get_summary(end, agent)

curr = start
path = []


def consult_validity(choice):
    links_str = format_options(graph[curr])
    ins = templates["valid"].format(links=links_str, choice=choice)
    out = agent.raw_prompt(ins)

    return out


def consult_loop(choice):
    path_str = format_options(path)

    ins = templates["loop"].format(
        desc=desc, goal=end, choice=choice, path=path_str)
    out = agent.raw_prompt(ins)

    ins = templates["visit ctx"].format(choice=choice, resp=out)
    out = agent.raw_prompt(ins, max_len=100)

    ins = templates["visit"].format(context=out, choice=choice)
    out = agent.raw_prompt(ins, max_len=100)

    return out


def consult_relativity(choice):
    ins = templates["related"].format(
        desc=desc, goal=end, choice=choice)
    out = agent.raw_prompt(ins, max_len=100)

    ins = templates["goodbad"].format(
        summary=out, choice=choice, goal=end)
    out = agent.raw_prompt(ins)

    return out


def consult_chain(iters):
    choice = ""
    bads = []

    for i in range(iters):
        ins = ""

        if i == 0:
            temp = templates["general"]
            links_str = format_options(graph[curr])
            ins = temp.format(desc=desc, goal=end,
                              links=links_str)
        else:
            temp = templates["consulted"]
            links_str = format_options(graph[curr] - set(bads))
            choices_str = format_options(bads)
            ins = temp.format(desc=desc, goal=end,
                              links=links_str, choices=choices_str)

        choice = agent.raw_prompt(ins)

        print("Which link do you pick?")
        print(choice)

        print("---")

        print(f"Testing choice: {choice}...")

        validity = consult_validity(choice)
        print(f"Valid? {validity}")

        visit = consult_loop(choice)
        print(f"Non-loopability? {visit}")

        relativity = consult_relativity(choice)
        print(f"Relatability? {relativity}")

        ins = templates["keep"].format(
            choice=choice, goal=end, relativity=relativity, validity=validity, loop=visit)
        out = agent.raw_prompt(ins)

        print(f"Decision to keep choice {choice}: {out}")
        print("-=-")

        if out.lower() == "yes":
            break

        bads.append(choice)

    return choice


print(f"Start: {start}, Goal: {end}")
print("===")

for i in range(10):
    path.append(curr)

    output = consult_chain(3)

    print(f"Final decision: {output}")
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
