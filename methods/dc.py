from math import ceil
from .singular import prompt_agent, validate_resp
from .ensemble import prompt_ensemble


def prompt_dc(max_per, agent, goal, links, desc, graph, template='general',
              bads=[], stack=False, ensemble_num=3):
    """Queries a hierarchy of agents for the next link

    Splits the possible links into groups of links, where the max number of
    links per group is determined by the max_per parameter. Agents are then
    queried with the smaller groups of links, and the chosen link is then sent
    up to be recursively split and grouped again. This repeats until 1 link
    remains. Invalid links or dead-ends are not sent up to the next level.

    Parameters
    ----------
    max_per : int
        The maximum number of links per group
    agent : AgentFlan
        The agent to query the prompt to
    goal : str
        The name of the goal Wikipedia page
    links : set or list
        The links available to click on the current page
    desc : str
        A summarized description of the goal Wikipedia page
    graph : defaultdict
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link
    template : str, optional
        Determines the template used for querying. Either 'general' or
        'consulted'.
    bads : list, optional
        A list of choices that the consulted method rejects. Only used if
        template is 'consulted'.
    stack : bool, optional
        Whether the DC is being used in a stack (each decision is an ensemble
        decision)
    ensemble_num : int, optional
        The number of agents that will give their votes

    Returns
    -------
    str
        The link that the agent suggests clicking on
    """

    pool = list(links)

    while len(pool) > 1:
        new_pool = []

        for i in range(ceil(len(pool) / max_per)):
            mini_pool = pool[i * max_per: min((i + 1) * max_per, len(pool))]

            output = ''

            if stack:
                output = prompt_ensemble(
                    ensemble_num, agent, goal, mini_pool, desc, template, bads)
            else:
                output = prompt_agent(
                    agent, goal, mini_pool, desc, template, bads)

            if validate_resp(output, '', goal, graph, mini_pool) < 0:
                continue

            new_pool.append(output)

        pool = new_pool
        print(pool)
        print("---")

    if len(pool) == 0:
        print("Decision failed. Pool size reached 0.")
        return ""

    return pool[0]
