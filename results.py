import json


def save_results(start, goal, bfs=None, astar=None, singular=None, ensemble=None, dc=None, consult=None, stack=None, path="results.json"):
    """Saves the results as a json file

    Parameters
    ----------
    start : str
        The start page
    goal : str
        The end/goal page
    bfs : list, optional
        The path that the BFS method followed
    astar : list, optional
        The path that the A* method followed
    singular : list, optional
        The path that the singular LLM method followed
    ensemble : list, optional
        The path that the ensemble method followed
    dc : list, optional
        The path that the divide and conquer method followed
    consult : list, optional
        The path that the consult method followed
    stack : list, optional
        The path that the stack method followed
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
