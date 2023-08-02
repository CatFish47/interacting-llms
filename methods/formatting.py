def top_border(c, width):
    lines = []

    lines.append(c * width)
    lines.append(c + ' ' * (width - 2) + c)

    return '\n'.join(lines)


def bot_border(c, width):
    lines = []

    lines.append(c + ' ' * (width - 2) + c)
    lines.append(c * width)

    return '\n'.join(lines)


def middle_txt(s, c, width):
    max_len = width - 4

    if len(s) > max_len:
        s = s[0:max_len - 3] + '...'

    s = s + ' ' * (max_len - len(s))

    return c + ' ' + s + ' ' + c


def format_title(s):
    """Formats string surround with # when printing
    """

    line_len = len(s) + 4
    lines = []

    lines.append(top_border('#', line_len))
    lines.append(middle_txt(s, '#', line_len))
    lines.append(bot_border('#', line_len))

    return '\n'.join(lines)


def format_results(path, width, goal, title):
    """Formats the results given the path"""

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

    lines.append(bot_border(c, width))

    return '\n'.join(lines)
