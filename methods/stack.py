from .consult import prompt_consult


def prompt_stack(agent, goal, links, desc, path, graph, iters=2, max_per=20,
                 ensemble_num=3):
    """Queries agents from consult, divide and conquer, and ensemble

    This will run the prompts through divide and conquer where each
    sub-decision is an ensemble decision. The final decision is then
    consulted and the process repeats if necessary.

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
    path : list
        A list of links that represents the path that the agent has traversed
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link
    iters : int, optional
        The maximum number of times the consultation will reject links
    max_per : int, optional
        The maximum number of links per group
    ensemble_num : int, optional
        The number of agents that will give their votes

    Returns
    -------
    str
        The link that the agent suggests clicking on
    """

    return prompt_consult(iters, agent, goal, links, desc, path, True, graph,
                          max_per, ensemble_num)
