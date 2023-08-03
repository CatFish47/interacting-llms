import json


def save_results(start, goal, bfs=None, astar=None, singular=None, ensemble=None, dc=None, consult=None, stack=None, path="results.json"):
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
