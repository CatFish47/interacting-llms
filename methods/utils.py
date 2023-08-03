import pickle
import random
from agents.flant5 import AgentFlan
import wikipediaapi
from .templates import templates


def get_graph(path):
    """Retrieves the graph from a path

    Parameters
    ----------
    path : str
        The path to the pkl file of the graphs

    Returns
    -------
    defaultdict
        The graph
    """

    graph = None

    # Read dictionary pkl file
    with open(path, 'rb') as fp:
        graph = pickle.load(fp)

    return graph


def get_pruned_graph(path):
    """Removes sink nodes from graph

    Removes nodes in graph that are dead-ends

    Parameters
    ----------
    path : str
        The path to the pkl file of the graph

    Returns
    -------
    defaultdict
        The pruned graph
    """

    graph = get_graph(path)

    explored_links = set(graph.keys())

    for src in graph.keys():
        ns = set()
        for dst in graph[src]:
            if dst in explored_links:
                ns.add(dst)

        graph[src] = ns

    return graph


def rand_start(graph):
    """Generates a start node given the graph

    Chooses a random non-sink vertex from the graph

    Parameters
    ----------
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link

    Returns
    -------
    str
        The name of the starting vertex
    """

    nodes = list(graph.keys())

    return nodes[random.randint(0, len(nodes) - 1)]


def rand_end(graph):
    """Generates an end node given the graph

    Chooses a random vertex from the graph

    Parameters
    ----------
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link

    Returns
    -------
    str
        The name of the ending vertex
    """

    explored_links = set(graph.keys())
    all_links = set()

    for key in explored_links:
        all_links = all_links | graph[key]

    all_links = list(all_links | explored_links)

    return all_links[random.randint(0, len(all_links) - 1)]


def format_options(opts):
    """Formats the options provided for the template

    Separates all options with a dash, space and a new line character.
    (e.g. "- Option 1")

    Parameters
    ----------
    opts : list, set
        All options in list/set format

    Returns
    -------
    str
        A description of the Wikipedia page
    """

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
        A description of the Wikipedia page
    """

    wiki_wiki = wikipediaapi.Wikipedia(
        f'Interacting LLM', 'en')

    page_py = wiki_wiki.page(page)
    desc = page_py.summary

    inputs = templates['summary'].format(page=page, desc=desc)
    summary = agent.raw_prompt(inputs, max_len=200)

    print(inputs)
    print(summary)
    print("===")

    return summary


def setup():
    """Sets up necessary variables for Wikirace

    Sets up the agent, graph, description, and start/end nodes.

    Returns
    -------
    (AgentFlan, str, str, str, defaultdict)
        A 5-tuple with (in order) the agent, start, end, description, and graph
    """

    agent = AgentFlan()

    graph = get_pruned_graph('wikiscrape/graph.pkl')
    start = rand_start(graph)
    end = rand_start(graph)
    start, end = ("The Bacon Cookbook", "Pinky and Perky")

    desc = get_summary(end, agent)

    return (agent, start, end, desc, graph)
