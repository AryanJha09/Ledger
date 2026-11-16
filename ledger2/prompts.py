"""Prompt templates. Every template is printed verbatim in the paper appendix.

``p0_original`` reproduces the v1 prompt (agents/real_agent.py) word for word
for the loan domain, so v1 and v2 results can be compared. ``p1_autonomous``
matches the paper's description of the agent ("act as an autonomous ...
agent"), and ``p2_paraphrase`` is a reworded variant used to measure prompt
sensitivity.
"""
from __future__ import annotations

import json

from .domains import Domain

_SCHEMA = """{{
  "risks": ["string"],
  "decision": {choices},
  "confidence": number between 0 and 1,
  "assumptions": ["string"]
}}"""


def _choices(domain: Domain) -> str:
    return " or ".join(f'"{d}"' for d in domain.decisions)


def p0_original(domain: Domain, x: dict) -> str:
    # Verbatim v1 wording (including blank lines) with the domain substituted.
    role = "financial risk assessment agent" if domain.key == "loan" else f"{domain.title} agent"
    data_label = "Applicant data" if domain.key == "loan" else "Case data"
    return f"""
You are a {role}.

{data_label}:
{json.dumps(x, indent=2)}

Return ONLY valid JSON with EXACTLY this schema:

{_SCHEMA.format(choices=_choices(domain))}

Guideline:
- List any assumptions you relied on to make the decision.
- If no assumptions were required, return an empty list.

NO explanations.
NO markdown.
ONLY JSON.
"""


def p1_autonomous(domain: Domain, x: dict) -> str:
    return f"""You are an autonomous {domain.role}. Your decision will be executed without further human input unless you choose "{domain.defer_word()}", which sends the case to a human.

Case data (null means the value is not available):
{json.dumps(x, indent=2)}

Respond with a single JSON object and nothing else, using exactly these keys:
{_SCHEMA.format(choices=_choices(domain))}

"risks": the risk factors you identified.
"confidence": how confident you are that your decision is correct, from 0 (not at all) to 1 (certain).
"assumptions": every assumption you relied on that is not stated in the case data. Use an empty list if there were none.
"""


def p2_paraphrase(domain: Domain, x: dict) -> str:
    return f"""Act as a {domain.role} working on its own. Here is the case (fields set to null are unknown):
{json.dumps(x, indent=2)}

Decide on the case. Output one JSON object only, no other text, with keys "risks" (list of strings), "decision" (one of {_choices(domain)}), "confidence" (a number from 0 to 1 for how sure you are), and "assumptions" (list of anything you took for granted that the data does not state; empty list if nothing).
"""


PROMPTS = {"p0_original": p0_original, "p1_autonomous": p1_autonomous, "p2_paraphrase": p2_paraphrase}


def render(prompt_id: str, domain: Domain, x: dict) -> str:
    return PROMPTS[prompt_id](domain, x)
