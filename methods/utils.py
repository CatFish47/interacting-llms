import pickle
import random
from agents.flant5 import AgentFlan
import wikipediaapi
from .templates import templates


def get_graph():
    graph = None

    # Read dictionary pkl file
    with open('wikiscrape/graph.pkl', 'rb') as fp:
        graph = pickle.load(fp)

    return graph


def get_pruned_graph():
    graph = get_graph()

    explored_links = set(graph.keys())

    for src in graph.keys():
        ns = set()
        for dst in graph[src]:
            if dst in explored_links:
                ns.add(dst)

        graph[src] = ns

    return graph


def get_graph_large():
    graph = None

    # Read dictionary pkl file
    with open('wikiscrape/archive/graph_large.pkl', 'rb') as fp:
        graph = pickle.load(fp)

    return graph


def rand_start(graph):
    '''
    This function generates a random start node from all nodes with outgoing edges
    '''
    nodes = list(graph.keys())

    return nodes[random.randint(0, len(nodes) - 1)]


def rand_end(graph):
    '''
    This function generates a random end node from all possible nodes in the graph
    '''
    explored_links = set(graph.keys())
    all_links = set()

    for key in explored_links:
        all_links = all_links | graph[key]

    all_links = list(all_links | explored_links)

    return all_links[random.randint(0, len(all_links) - 1)]


def format_options(opts):
    return "- " + "\n- ".join(opts)


def get_summary(page, agent):
    """Queries the agent for a summary of the Wikipedia page

    Gets the summary of the Wikipedia page using the Wikipedia API, then gets
    the agent to summarize it

    Parameters
    ----------
    page : str
        The page to be summarized
    agent : AgentFlan
        The agent that will summarize the page

    Returns
    -------
    str
        Returns a string of the description of the Wikipedia page
    """

    wiki_wiki = wikipediaapi.Wikipedia(
        f'Interacting LLM', 'en')

    page_py = wiki_wiki.page(page)
    desc = page_py.summary

    inputs = templates['summary'].format(page=page, desc=desc)
    summary = agent.raw_prompt(inputs, max_len=200)

    return summary


def setup():
    agent = AgentFlan()

    graph = get_pruned_graph()
    # start = rand_start(graph)
    # end = rand_start(graph)
    start, end = ("Bacon soup", "Ostrich meat")

    desc = get_summary(end, agent)

    return (agent, start, end, desc, graph)
