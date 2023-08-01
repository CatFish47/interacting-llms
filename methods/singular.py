from .utils import format_options
from .templates import templates


def prompt_agent(agent, goal, links, desc, template='general', bads=[]):
    """Queries the agent for the next link

    Prompts the agent for a link by providing it with information regarding
    links available and its goal.

    Parameters
    ----------
    agent : AgentFlan
        The agent to query the prompt to
    goal : str
        The name of the goal Wikipedia page
    links : set or list
        The links available to click on the current page
    desc : str
        A summarized description of the goal Wikipedia page
    template : str, optional
        Determines the template used for querying. Either 'general' or
        'consulted'.
    bads : list, optional
        A list of choices that the consulted method rejects. Only used if
        template is 'consulted'.

    Returns
    -------
    str
        The link that the agent suggests clicking on
    """

    links_str = format_options(links)
    bads_str = format_options(bads)

    inputs = templates[template].format(
        goal=goal, links=links_str, desc=desc, choices=bads_str)
    output = agent.raw_prompt(inputs)

    return output


def validate_resp(resp, curr, goal, graph, links=None):
    """Validates a link

    Checks if the link outputted by an agent is valid, a dead-end, or the goal

    TODO: differentiate between invalid link and dead-end

    Parameters
    ----------
    resp : str
        The link that the agent suggests clicking on
    curr : str
        The page that the agent is currently on
    goal : str
        The name of the goal Wikipedia page
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link
    links : list/set, optional
        A list or set of links. By default is None. If no set/list of links
        are provided, it will be set to the set of links available to click
        from the current page curr

    Returns
    -------
    int
        Outputs -1 for an invalid link, 1 if the response is the goal, or 0 if
        neither
    """
    if links is None:
        links = graph[curr]

    if resp not in links or len(graph[resp]) == 0:
        return -1

    if resp == goal:
        return 1

    return 0
