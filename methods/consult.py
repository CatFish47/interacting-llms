from .utils import format_options
from .templates import templates
from .singular import prompt_agent
from .dc import prompt_dc


def consult_validity(agent, links, choice):
    """Consultation for if the chosen link is valid

    Parameters
    ----------
    agent : AgentFlan
        The agent to query the prompt to
    links : set/list
        The set of links that the agent had a choice from
    choice : str
        The choice that the previous agent chose

    Returns
    -------
    str
        "valid" or "invalid" depending on if the link was valid or not
    """
    links_str = format_options(links)
    ins = templates["valid"].format(links=links_str, choice=choice)
    out = agent.raw_prompt(ins)

    return out


def consult_loop(agent, goal, choice, desc, path):
    """Consultation for if the chosen link will cause a loop

    Parameters
    ----------
    agent : AgentFlan
        The agent to query the prompt to
    goal : str
        The name of the goal Wikipedia page
    choice : str
        The choice that the previous agent chose
    desc : str
        A summarized description of the goal Wikipedia page
    path : list
        A list of links that represents the path that the LLM has traversed

    Returns
    -------
    str
        "good" or "bad" depending on if the choice will cause a loop or is
        necessary regardless
    """
    path_str = format_options(path)

    ins = templates["loop"].format(
        desc=desc, goal=goal, choice=choice, path=path_str)
    out = agent.raw_prompt(ins)

    ins = templates["visit ctx"].format(choice=choice, resp=out)
    out = agent.raw_prompt(ins, max_len=100)

    ins = templates["visit"].format(context=out, choice=choice)
    out = agent.raw_prompt(ins)

    return out


def consult_relativity(agent, goal, choice, desc):
    """Consultation for if the chosen link is related to the goal

    Parameters
    ----------
    agent : AgentFlan
        The agent to query the prompt to
    goal : str
        The name of the goal Wikipedia page
    choice : str
        The choice that the previous agent chose
    desc : str
        A summarized description of the goal Wikipedia page

    Returns
    -------
    str
        "related" or "unrelated" depending on if the choice was related or not
    """
    ins = templates["related"].format(
        desc=desc, goal=goal, choice=choice)
    out = agent.raw_prompt(ins, max_len=200)

    ins = templates["goodbad"].format(
        summary=out, choice=choice, goal=goal)
    out = agent.raw_prompt(ins)

    return out


def prompt_consult(iters, agent, goal, links, desc, path, stack=False,
                   graph=None, max_per=20, ensemble_num=3):
    """Queries a series of consultation agents for the next link

    This will ask agents to determine the validity, loopability, and relativity
    of a link in relation to its goal and will determine if it will pick a new
    link.

    Parameters
    ----------
    iters : int
        The maximum number of times the consultation will reject links
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
    stack : bool, optional
        Whether the DC is being used in a stack (each decision is an ensemble
        decision)
    graph : defaultdict, optional
        A dictionary where the key is a link and the value is a set containing
        all possible links from the key link
    max_per : int, optional
        The maximum number of links per group
    ensemble_num : int, optional
        The number of agents that will give their votes

    Returns
    -------
    str
        The link that the agent suggests clicking on
    """

    choice = ""
    bads = []

    for i in range(iters):
        temp = 'general' if i == 0 else 'consulted'

        choice = ''

        if stack:
            choice = prompt_dc(max_per, agent, goal, links, desc,
                               graph, temp, bads, stack, ensemble_num)
        else:
            choice = prompt_agent(agent, goal, links, desc, temp, bads)

        print("Which link do you pick?")
        print(choice)

        print("---")

        print(f"Testing choice: {choice}...")

        validity = consult_validity(agent, links, choice)
        print(f"Valid? {validity}")

        visit = consult_loop(agent, goal, choice, desc, path)
        print(f"Non-loopability? {visit}")

        relativity = consult_relativity(agent, goal, choice, desc)
        print(f"Relatability? {relativity}")

        ins = templates["keep"].format(
            choice=choice, goal=goal, relativity=relativity,
            validity=validity, loop=visit)
        out = agent.raw_prompt(ins)

        print(f"Decision to keep choice {choice}: {out}")
        print("-=-")

        if out.lower() == "yes":
            break

        bads.append(choice)

    return choice
