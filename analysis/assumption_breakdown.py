import json
from pathlib import Path
from collections import Counter, defaultdict

from diagnostics.assumption_types import classify_assumptions

LOG_BASE = Path("experiments/logs")

def classify_assumption(text: str) -> str:
    """
    Classify an assumption into epistemic severity categories.

    Returns one of: benign, escalated, degenerate
    """
    if not text or not isinstance(text, str):
        return "degenerate"

    t = text.lower()

    # Degenerate / malformed outputs
    if "invalid structured output" in t or "n/a" in t:
        return "degenerate"

    # Escalated / speculative reasoning
    escalated_markers = [
        "might",
        "could",
        "likely",
        "future",
        "potential",
        "expected",
        "may increase",
        "may decrease",
        "stability",
        "growth"
    ]
    if any(m in t for m in escalated_markers):
        return "escalated"

    # Otherwise treat as benign
    return "benign"


def analyze_model(model_dir: Path):
    counts = Counter()
    by_case_type = defaultdict(Counter)

    for run_file in model_dir.glob("run_*.json"):
        with open(run_file) as f:
            run = json.load(f)

        case_type = run.get("case_type", "unknown")
        assumptions = run.get("agent_output", {}).get("assumptions", [])

        if not assumptions:
            continue

        types = classify_assumptions(assumptions)

        for t in types:
            counts[t] += 1
            by_case_type[case_type][t] += 1

    return counts, by_case_type


if __name__ == "__main__":
    for model_dir in sorted(LOG_BASE.iterdir()):
        if not model_dir.is_dir():
            continue

        print("\n" + "=" * 60)
        print(f"MODEL: {model_dir.name}")

        counts, by_case = analyze_model(model_dir)

        print("\nOVERALL ASSUMPTION TYPES")
        for k, v in counts.items():
            print(f"  {k}: {v}")

        print("\nBREAKDOWN BY CASE TYPE")
        for case, c in by_case.items():
            print(f"  {case}: {dict(c)}")
