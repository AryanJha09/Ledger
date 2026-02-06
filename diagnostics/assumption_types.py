from typing import List

FUTURE_MARKERS = [
    "might", "may", "could", "likely", "potential",
    "in the future", "over time", "eventually"
]

DEGENERATE_MARKERS = [
    "invalid", "structured output", "n/a", "unknown", "error"
]


def classify_assumption(text: str) -> str:
    text_lower = text.lower()

    # Degenerate first (strongest signal)
    if any(marker in text_lower for marker in DEGENERATE_MARKERS):
        return "degenerate"

    # Escalated (epistemic overreach)
    if any(marker in text_lower for marker in FUTURE_MARKERS):
        return "escalated"

    # Otherwise benign
    return "benign"


def classify_assumptions(assumptions: List[str]) -> List[str]:
    return [classify_assumption(a) for a in assumptions]
