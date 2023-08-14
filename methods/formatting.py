def top_border(c, width):
    """Returns the top border of the string

    Returns two lines of strings, the first which is a row of the border
    character and the second line being the border character on each side
    with empty space in between.

    Parameters
    ----------
    c : str
        The character that will be used as the border
    width : int
        The maximum length of the string

    Returns
    -------
    str
        The formatted top border string
    """

    lines = []

    lines.append(c * width)
    lines.append(c + ' ' * (width - 2) + c)

    return '\n'.join(lines)


def bot_border(c, width):
    """Returns the bottom border of the string

    Returns two lines of strings, the first which is the border character on
    each side with empty space in between and the second line being a row of
    the border character.

    Parameters
    ----------
    c : str
        The character that will be used as the border
    width : int
        The maximum length of the string

    Returns
    -------
    str
        The formatted bottom border string
    """

    lines = []

    lines.append(c + ' ' * (width - 2) + c)
    lines.append(c * width)

    return '\n'.join(lines)


def middle_txt(s, c, width):
    """Formats string to surround just the sides with border character

    Formats the string by adding the border character to the sides. For
    example, "Text" would turn into "* Text  *" with a border character
    of "*" and a width of 10. If the length of the string would cause the
    width to exceed the maximum width set in the parameter, the string will
    be truncated, which will be indicated by a "..."

    Parameters
    ----------
    s : str
        The content of the string
    c : str
        The character that will be used as the border
    width : int
        The maximum length of the string

    Returns
    -------
    str
        The formatted string
    """

    max_len = width - 4

    if len(s) > max_len:
        s = s[0:max_len - 3] + '...'

    s = s + ' ' * (max_len - len(s))

    return c + ' ' + s + ' ' + c


def format_title(s):
    """Formats string surround with # when printing

    Parameters
    ----------
    s : str
        The title to be surrounded in a #

    Returns
    -------
    str
        The formatted string ready to print
    """

    line_len = len(s) + 4
    lines = []

    lines.append(top_border('#', line_len))
    lines.append(middle_txt(s, '#', line_len))
    lines.append(bot_border('#', line_len))

    return '\n'.join(lines)


def format_results(results, width, goal, title):
    """Formats results of a runned method and includes information on the run

    Formats the results in console for easy reading. Surrounds the results in
    "*" and contains information of the path followed, whether the goal was
    reached, and the number of links visited before terminating.

    Parameters
    ----------
    results : dict
        The dictionary results that includes the path, the time taken, and the
        number of times the agent was queried
    width : int
        The maximum length of the string
    goal : str
        The goal page
    title : str
        The title of the results

    Returns
    -------
    str
        The formatted results, ready to print
    """

    path = results["path"]
    time_taken = results["time"]
    queries = results["prompts"]
    goal_reach = "Yes" if len(path) == 0 or goal == path[-1] else "No"

    c = '*'
    lines = []

    lines.append(top_border(c, width))

    lines.append(middle_txt(title, c, width))
    lines.append(middle_txt('', c, width))

    lines.append(middle_txt('Path:', c, width))
    for p in path:
        lines.append(middle_txt(f"  - {p}", c, width))

    lines.append(middle_txt('', c, width))

    lines.append(middle_txt(f'Reached goal? {goal_reach}', c, width))
    lines.append(middle_txt(f'# of links: {len(path)}', c, width))
    lines.append(middle_txt(f'Time taken: {time_taken}', c, width))
    lines.append(middle_txt(f'# of queries: {queries}', c, width))

    lines.append(bot_border(c, width))

    return '\n'.join(lines)
