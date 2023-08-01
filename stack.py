from agents.flant5 import AgentFlan
from utils import rand_start, rand_end, get_pruned_graph, get_summary, format_options
from math import ceil
from templates import templates
from random import shuffle
from collections import Counter

agent = AgentFlan()

graph = get_pruned_graph()
start = rand_start(graph)
end = rand_start(graph)
start, end = ("Bacon soup", "Ostrich meat")

desc = get_summary(end, agent)

print(desc)
print('===')

curr = start
path = []
bads = []


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


def consult_chain(iters=3, max_per=20, ensemble_size=3):
    choice = ""
    bads = []

    for i in range(iters):
        ins = ""

        if i == 0:
            temp = "general"
        else:
            temp = "consulted"

        choice = decide(graph[curr], max_per, ensemble_size, temp)

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


def get_ensemble(links, num, template):
    links = list(links)
    cnt = Counter()

    for i in range(num):
        shuffle(links)
        links_str = format_options(links)

        inputs = ""

        if template == 'general':
            inputs = templates[template].format(
                goal=end, links=links_str, desc=desc)
        if template == 'consulted':
            bads_str = format_options(bads)
            inputs = templates[template].format(
                goal=end, links=links_str, desc=desc, choices=bads_str)

        output = agent.raw_prompt(inputs)

        inputs_conf = templates["confidence"].format(
            goal=end, choice=output, desc=desc)
        output_conf = int(agent.raw_prompt(inputs_conf))

        cnt[output] += output_conf

    print(cnt.most_common())

    return cnt.most_common(1)[0][0]


def decide(links, max_per, ensemble_size, template='general'):
    pool = list(links)

    while len(pool) > 1:
        new_pool = []

        for i in range(ceil(len(pool) / max_per)):
            mini_pool = pool[i * max_per: min((i + 1) * max_per, len(pool))]

            output = get_ensemble(mini_pool, ensemble_size, template)

            if output not in mini_pool or len(graph[output]) == 0:
                continue

            new_pool.append(output)

        pool = new_pool
        print("---")
        print(pool)
        print("-=-")

    if len(pool) == 0:
        print("Decision failed. Pool size reached 0.")
        return ""

    return pool[0]


print(f"Start: {start}, Goal: {end}")
print('===')

for i in range(10):
    path.append(curr)

    output = consult_chain(iters=3, max_per=20, ensemble_size=3)

    print(f"Final decision: {output}")

    print("===")

    if output == "":
        break

    if output == end:
        path.append(end)
        break

    curr = output

print(path)
