import json


def save_results(start, goal, bfs=None, astar=None, singular=None, ensemble=None, dc=None, consult=None, stack=None, path="results.json"):
    """Saves the results as a json file

    Parameters
    ----------
    start : str
        The start page
    goal : str
        The end/goal page
    bfs : dict, optional
        The results of the BFS method
    astar : dict, optional
        The results of the A* method
    singular : dict, optional
        The results of the singular LLM method
    ensemble : dict, optional
        The results of the ensemble method
    dc : dict, optional
        The results of the divide and conquer method
    consult : dict, optional
        The results of the consult method
    stack : dict, optional
        The results of the stack method
    path : str, optional
        The file path to save the file to. By default, it is "results.json"

    Returns
    -------
    dict
        The json in dictionary form
    """

    data = None

    try:
        with open('results.json', 'r') as file_object:
            data = json.load(file_object)
    except FileNotFoundError as e:
        data = {'data': []}

    methods = ['bfs', 'astar', 'singular',
               'ensemble', 'dc', 'consult', 'stack']
    metrics = ['path', 'time', 'prompts']

    results = {
        'start': start,
        'goal': goal,
        'bfs': bfs,
        'astar': astar,
        'singular': singular,
        'ensemble': ensemble,
        'dc': dc,
        'consult': consult,
        'stack': stack
    }

    data['data'].append(results)

    with open(path, 'w') as file_object:
        json.dump(data, file_object)

    return data
