import wikipediaapi
import pickle
from collections import deque, defaultdict


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
    if iteration == total:
        print()


def blacklisted_title(title):
    banned_words = ["Portal:", "User:", "Wikipedia:",
                    "Help:", "Template:", "Module:", "Template talk:", "File:"]
    for w in banned_words:
        if w in title:
            return True

    return False


def link_degrees(start, degrees):
    wiki_wiki = wikipediaapi.Wikipedia(
        f'{degrees} Degrees of Bacon', 'en')
    all_links = set()
    queue = deque()
    graph = defaultdict(set)

    queue.append(start)

    char_lim = 20

    for i in range(degrees + 1):
        print(f'Exploring degree #{i}')
        iter_size = len(queue)
        j = 0
        while j < iter_size:
            # for j in range(iter_size):
            title = queue.popleft()
            print_progress_bar(
                j, iter_size, suffix=f"{j}/{iter_size-1} {title[0:char_lim].ljust(char_lim)}")

            j += 1

            if title in all_links:
                continue

            if blacklisted_title(title):
                continue

            all_links.add(title)

            if (i == degrees):
                continue

            try:
                page = wiki_wiki.page(title)
            except TimeoutError as e:
                j -= 1
                queue.appendleft(title)
                print('')
                print('Request timed out... retrying')
                continue

            links = page.links
            for l in links.keys():
                queue.append(l)
                graph[title].add(l)

        print_progress_bar(iter_size, iter_size)

    print(
        f'There are {len(all_links)} links reachable within {degrees} degrees of {start}')

    return graph


wiki_graph = link_degrees("Bacon", 3)
with open("graph.pkl", "wb") as fp:
    pickle.dump(wiki_graph, fp)
    print("Graph successfully saved to graph.txt")
