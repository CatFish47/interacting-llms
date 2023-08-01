import wikipediaapi
import pickle
from collections import deque


def blacklisted_title(title):
    banned_words = ["Portal:", "User:", "Wikipedia:",
                    "Help:", "Template:", "Module:", "Template talk:", "File:"]
    for w in banned_words:
        if w in title:
            return True

    return False

# Print iterations progress


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def extend(graph):
    wiki_wiki = wikipediaapi.Wikipedia(
        f'More Degrees of Bacon (gxcheng@ucsd.edu)', 'en')

    explored_links = set(graph.keys())
    all_links = set()
    unexplored_links = set()
    queue = deque()

    for key in explored_links:
        all_links = all_links | graph[key]

    unexplored_links = all_links - explored_links

    for unexplored in unexplored_links:
        queue.append(unexplored)

    char_lim = 20

    print(f'Exploring degree')
    iter_size = len(queue)
    i = 0

    while i < iter_size:
        title = queue.popleft()
        print_progress_bar(
            i, iter_size, suffix=f"{i}/{iter_size-1} {title[0:char_lim].ljust(char_lim)}")

        i += 1

        if title in explored_links:
            continue

        if blacklisted_title(title):
            continue

        try:
            page = wiki_wiki.page(title)
            explored_links.add(title)
        except TimeoutError as e:
            i -= 1
            queue.appendleft(title)
            print('')
            print('Request timed out... retrying')
            continue

        links = page.links
        for l in links.keys():
            queue.append(l)
            graph[title].add(l)

    print_progress_bar(iter_size, iter_size)

    return graph


graph = None

# Read dictionary pkl file
with open('graph.pkl', 'rb') as fp:
    graph = pickle.load(fp)

graph = extend(graph)

with open("graph.pkl", "wb") as fp:
    pickle.dump(graph, fp)
    print("Graph successfully saved to graph.txt")
