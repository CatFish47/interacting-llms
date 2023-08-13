general_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". "{goal}" is summarized by the following: {desc}

OPTIONS:
{links}

Select the option most related to "{goal}".
"""

loop_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page.

You've been to these links before:
{path}

OPTIONS:
- yes
- no

Have you visited "{choice}" before?
"""

visit_ctx_template = """
Context: Have you been to "{choice}" before? {resp}.

OPTIONS:
- You have been to "{choice}" before, which means it is a terrible idea to go again because you have already been there.
- You have not been to "{choice}" before, which means that it is an amazing idea to go to "{choice}" because then you can explore everything that is there.

Which option is the most applicable?
"""

visit_template = """
Context: {context}

OPTIONS:
- good
- bad

Is it good or bad to visit "{choice}"?
"""

valid_template = """
Context: You are given the following list of choices:
{links}

OPTIONS:
- valid
- invalid

Is "{choice}" a valid choice?
"""

rel_template = """
Context: You are trying to determine if "{choice}" is related to "{goal}". "{goal}" is summarized by the following: {desc}

How are "{choice}" and "{goal}" related or unrelated. Provide reasoning.
"""

conf_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". "{goal}" is summarized by the following: {desc}

Here's what each number of the confidence scale means:
A 1 means that you are certain that "{choice}" and "{goal}" have nothing to do with each other.
A 2 means that "{choice}" and "{goal}" are probably not related.
A 3 means that you think "{choice}" could be related to "{goal}".
A 4 means that are are certain that "{choice}" and "{goal}" are related.
A 5 means that "{choice}" and "{goal}" are the same.

OPTIONS: 1, 2, 3, 4, 5

Rate your confidence on a scale of 1 to 5 that "{choice}" is related to or the same as "{goal}".
"""

summary_template = """
Context: Here is the Wikipedia summary for the page "{page}": {desc}

What is "{page}"?
"""

goodbad_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}".

You have determined this about the relationship between "{choice}" and "{goal}": {summary}

OPTIONS:
- related
- unrelated

Is "{choice}" a related or unrelated choice to get to "{goal}"?
"""

keep_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". You chose the link "{choice}".

Finally, whether a link is related or not to the goal "{goal}" is important too, otherwise you might not get there. Based on relatedness, it has been determined that "{choice}" is a {relativity} choice.
The validity of a link is the most important, since if the link isn't valid you can't click it. "{choice}" is a {validity} link.
Visiting a link previously is also important, since we want to avoid loops. You've determined that "{choice}" is a {loop} decision.

OPTION:
- yes
- no

Would you like to keep your choice, "{choice}"?
"""

consulted_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". "{goal}" is summarized by the following: {desc}

Bad options:
{choices}

Good options:
{links}

From the options pick the one closest to "{goal}".
"""

templates = {
    "general": general_template,
    "loop": loop_template,
    "related": rel_template,
    "confidence": conf_template,
    "summary": summary_template,
    "keep": keep_template,
    "goodbad": goodbad_template,
    "consulted": consulted_template,
    "valid": valid_template,
    "visit ctx": visit_ctx_template,
    "visit": visit_template
}
