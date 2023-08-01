general_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". "{goal}" is summarized by the following: {desc}

OPTIONS:
{links}

From the options, pick the one closest to "{goal}".
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
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to "{goal}". "{goal}" is summarized by the following: {desc}

How are "{choice}" and "{goal}" related or unrelated? Provide reasoning.
"""

conf_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". "{goal}" is summarized by the following: {desc}

OPTIONS: 1, 2, 3, 4, 5

Where 1 is least confident and 5 is most confident, rate your confidence on a scale of 1 to 5 that "{choice}" is related to "{goal}".
"""

summary_template = """
Context: Here is the Wikipedia summary for the page "{page}": {desc}

What is "{page}"?
"""

goodbad_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}".

{summary}

OPTIONS:
- related
- unrelated

Is "{choice}" a related or unrelated choice to get to "{goal}"?
"""

keep_template = """
Context: You are playing Wikipedia race, a game where you try to get from one Wikipedia page to another by only clicking links on the Wikipedia page. Your goal is to get to the page "{goal}". You chose the link "{choice}".

The validity of a link is very important, since if the link isn't valid you can't click it. Is "{choice}" a valid link? {validity}
Visiting a link previously is also important, since we want to avoid loops. Based on previously visited links, you've determined that "{choice}" is a {loop} decision.
Finally, whether a link is related or not to the goal "{goal}" is important too, otherwise you might not get there. Based on relativity, it has been determined that "{choice}" is a {relativity} choice.

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
