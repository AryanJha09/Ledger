import json
from pathlib import Path
from collections import defaultdict, Counter

from analysis.assumption_breakdown import classify_assumption

LOG_ROOT = Path("experiments/logs")


def analyze():
    results = defaultdict(lambda: defaultdict(Counter))
    totals = defaultdict(lambda: defaultdict(int))

    for model_dir in LOG_ROOT.iterdir():
        if not model_dir.is_dir():
            continue

        model = model_dir.name

        for run_file in model_dir.glob("run_*.json"):
            with open(run_file) as f:
                run = json.load(f)

            case_type = run.get("case_type")
            assumptions = run.get("agent_output", {}).get("assumptions", [])

            for a in assumptions:
                label = classify_assumption(a)
                results[model][case_type][label] += 1
                totals[model][case_type] += 1

    return results, totals


def normalize(results, totals):
    percentages = defaultdict(lambda: defaultdict(dict))

    for model in results:
        for case_type in results[model]:
            total = totals[model][case_type]
            if total == 0:
                continue

            for label, count in results[model][case_type].items():
                percentages[model][case_type][label] = round(
                    100 * count / total, 1
                )

    return percentages


def print_tables(percentages):
    for model in sorted(percentages.keys()):
        print(f"\nMODEL: {model}")
        print("Case Type      | Benign (%) | Escalated (%) | Degenerate (%)")
        print("------------------------------------------------------------")

        for case_type in sorted(percentages[model].keys()):
            benign = percentages[model][case_type].get("benign", 0.0)
            escalated = percentages[model][case_type].get("escalated", 0.0)
            degenerate = percentages[model][case_type].get("degenerate", 0.0)

            print(
                f"{case_type:<14} | "
                f"{benign:>10.1f} | "
                f"{escalated:>13.1f} | "
                f"{degenerate:>14.1f}"
            )


if __name__ == "__main__":
    results, totals = analyze()
    percentages = normalize(results, totals)
    print_tables(percentages)
