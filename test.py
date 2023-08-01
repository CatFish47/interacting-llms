import methods.methods as m

agent, start, end, desc, graph = m.setup()

curr = start
path = []

print(f"Start: {start}, Goal: {end}")
print("===")

# path = m.bfs(graph, start, end)
# print(path)

for i in range(10):
    path.append(curr)

    links = graph[curr]

    # resp = m.prompt_agent(agent, end, links, desc)
    # resp = m.prompt_ensemble(3, agent, end, links, desc)
    # resp = m.prompt_dc(10, agent, end, links, desc, graph)
    # resp = m.prompt_consult(3, agent, end, links, desc, path)
    resp = m.prompt_stack(agent, end, links, desc, path, graph)

    print(f"Decision: {resp}")
    print("-=-")

    validity = m.validate_resp(resp, curr, end, graph)

    if validity < 0:
        print(f"Agent has responded with an invalid link: {resp}")
        break

    if validity > 0:
        path.append(resp)
        print("The end has been reached!")
        break

    curr = resp

print(path)
