import json
import math
from pathlib import Path
from collections import Counter, defaultdict

BASE_LOG_DIR = Path("experiments/logs")
assert BASE_LOG_DIR.exists(), "Log directory not found"


def analyze_model(model_dir: Path):
    runs = []

    for f in sorted(model_dir.glob("run_*.json")):
        with f.open(encoding="utf-8") as fp:
            runs.append(json.load(fp))

    N = len(runs)
    assert N > 0, f"No runs found for model {model_dir.name}"

    # --- Aggregates ---
    signal_counts = Counter()
    decision_counts = Counter()
    confidence_all = []

    confidence_by_signal = defaultdict(list)
    confidence_without_signal = defaultdict(list)

    for run in runs:
        agent_output = run.get("agent_output", {})
        diagnostics = run.get("diagnostics", [])

        decision = agent_output.get("decision")
        confidence = agent_output.get("confidence")

        if decision is None or confidence is None:
            continue  # skip malformed runs safely

        decision_counts[decision] += 1
        confidence_all.append(confidence)

        # Track confidence conditioned on signals
        if diagnostics:
            for signal in diagnostics:
                signal_counts[signal] += 1
                confidence_by_signal[signal].append(confidence)
        else:
            # runs with *no* diagnostics count as "without" for all observed signals
            for signal in signal_counts.keys():
                confidence_without_signal[signal].append(confidence)

    return {
        "total_runs": N,
        "signal_counts": signal_counts,
        "decision_counts": decision_counts,
        "confidence_all": confidence_all,
        "confidence_by_signal": confidence_by_signal,
        "confidence_without_signal": confidence_without_signal,
    }


def print_results(model_name, results):
    N = results["total_runs"]

    print("\n==============================")
    print(f"MODEL: {model_name}")
    print(f"TOTAL RUNS: {N}")

    print("\nMODEL BEHAVIOR SIGNAL RATES")
    print("-" * 50)
    for signal, count in results["signal_counts"].items():
        print(f"{signal:30s} {count:3d}  ({count / N:.3f})")

    print("\nDECISION DISTRIBUTION")
    print("-" * 50)
    for decision, count in results["decision_counts"].items():
        print(f"{decision:15s} {count:3d}  ({count / N:.3f})")

    print("\nCONFIDENCE STATISTICS")
    print("-" * 50)
    mean_confidence = sum(results["confidence_all"]) / len(results["confidence_all"])
    print(f"Overall mean confidence: {mean_confidence:.3f}\n")

    for signal, vals in results["confidence_by_signal"].items():
        mean_with = sum(vals) / len(vals)

        without_vals = results["confidence_without_signal"].get(signal, [])
        mean_without = (
            sum(without_vals) / len(without_vals)
            if without_vals
            else math.nan
        )

        print(
            f"{signal:30s} "
            f"with signal: {mean_with:.3f} | without: {mean_without:.3f}"
        )

def export_results(all_results, out_path):
    serializable = {}
    for model, r in all_results.items():
        serializable[model] = {
            "total_runs": r["total_runs"],
            "signal_counts": dict(r["signal_counts"]),
            "decision_counts": dict(r["decision_counts"]),
            "mean_confidence": (
                sum(r["confidence_all"]) / len(r["confidence_all"])
                if r["confidence_all"] else 0.0
            ),
        }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


if __name__ == "__main__":
    all_results = {}
    for model_dir in sorted(BASE_LOG_DIR.iterdir()):
        if not model_dir.is_dir():
            continue
        results = analyze_model(model_dir)
        all_results[model_dir.name] = results
        print_results(model_dir.name, results)

    export_results(all_results, Path("analysis/model_summary.json"))
