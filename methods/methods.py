from .utils import setup
from .bfs import bfs
from .singular import prompt_agent, validate_resp
from .ensemble import prompt_ensemble
from .dc import prompt_dc
from .consult import prompt_consult
from .stack import prompt_stack
import time


def run_method(method, agent, start, end, desc, graph, iters=10):
    """Runs a specific LLM method

    Runs a method to continuously ask the method for the next suggested link
    to click.

    Parameters
    ----------
    method : str
        The method to use. Choice between 'singular', 'ensemble', 'dc',
        'consult', and 'stack'
    agent : Agent
        The agent to ask the questions to
    start : str
        The start page
    end : str
        The goal page
    desc : str
        The description of the goal page
    graph : defaultdict
        The graph that provides all possible links to click from a given page
    iters : int, optional
        The maximum number of times that the method should be prompted which
        link it thinks it should click

    Returns
    -------
    dict
        The dictionary results that includes the path, the time taken, and the
        number of times the agent was queried
    """

    start_time = time.time()
    total_prompts = 0

    curr = start
    path = [curr]

    for i in range(iters):
        resp = ""
        num_prompts = 0

        links = graph[curr]

        if method == 'singular':
            resp, num_prompts = prompt_agent(agent, end, links, desc)
        elif method == 'ensemble':
            resp, num_prompts = prompt_ensemble(3, agent, end, links, desc)
        elif method == 'dc':
            resp, num_prompts = prompt_dc(10, agent, end, links, desc, graph)
        elif method == 'consult':
            resp, num_prompts = prompt_consult(
                3, agent, end, links, desc, path)
        elif method == 'stack':
            resp, num_prompts = prompt_stack(
                agent, end, links, desc, path, graph, iters=2)
        else:
            resp, num_prompts = ("", 0)
            print("Invalid method")

        print(f">> Decision: {resp}")
        print("-=-")

        total_prompts += num_prompts
        path.append(resp)
        validity = validate_resp(resp, curr, end, graph)

        if validity < 0:
            print(f"Agent has responded with an invalid link: {resp}")
            break

        if validity > 0:
            print("The end has been reached!")
            break

        curr = resp

    end_time = time.time()

    res = {
        "path": path,
        "time": end_time - start_time,
        "prompts": total_prompts
    }

    return res
