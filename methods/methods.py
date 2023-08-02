from .utils import setup
from .bfs import bfs
from .singular import prompt_agent, validate_resp
from .ensemble import prompt_ensemble
from .dc import prompt_dc
from .consult import prompt_consult
from .stack import prompt_stack


def run_method(method, agent, start, end, desc, graph, iters=10):
    curr = start
    path = [curr]

    for i in range(iters):
        resp = ""

        links = graph[curr]

        if method == 'singular':
            resp = prompt_agent(agent, end, links, desc)
        elif method == 'ensemble':
            resp = prompt_ensemble(3, agent, end, links, desc)
        elif method == 'dc':
            resp = prompt_dc(10, agent, end, links, desc, graph)
        elif method == 'consult':
            resp = prompt_consult(3, agent, end, links, desc, path)
        elif method == 'stack':
            resp = prompt_stack(agent, end, links, desc, path, graph)
        else:
            resp = ""
            print("Invalid method")

        print(f">> Decision: {resp}")
        print("-=-")

        path.append(resp)
        validity = validate_resp(resp, curr, end, graph)

        if validity < 0:
            print(f"Agent has responded with an invalid link: {resp}")
            break

        if validity > 0:
            print("The end has been reached!")
            break

        curr = resp

    return path
