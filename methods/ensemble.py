from collections import Counter
from .templates import templates
from .singular import prompt_agent


def prompt_ensemble(num, agent, goal, links, desc, template='general',
                    bads=[]):
    """Queries an ensemble of agents for the next link

    Prompts multiple agents for a link by providing it with information
    regarding links available and its goal. Each agent will then give a
    confidence score between 1-5 in regards to their choice and the choice
    with the most confidence.

    Parameters
    ----------
    num : int
        The number of agents that will give their votes
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
    str, int
        The link that the agent suggests clicking on and the number of times
        the agent was prompted
    """

    cnt = Counter()

    tot_prompts = 0

    for _ in range(num):
        output, num_prompts = prompt_agent(
            agent, goal, links, desc, template, bads)

        inputs_conf = templates["confidence"].format(goal=goal, choice=output,
                                                     desc=desc)
        output_conf = int(agent.raw_prompt(inputs_conf))
        num_prompts += 1

        cnt[output] += output_conf
        tot_prompts += 1

    print(cnt.most_common())

    return cnt.most_common(1)[0][0], tot_prompts
