import json
from pathlib import Path
from collections import Counter

from diagnostics.signals import detect_failure_signals

LOG_ROOT = Path("experiments/logs")


def summarize_from_logs():
    all_results = {}

    for model_dir in sorted(LOG_ROOT.iterdir()):
        if not model_dir.is_dir():
            continue

        model = model_dir.name
        signal_counter = Counter()
        total_cases = 0

        for run_file in sorted(model_dir.glob("run_*.json")):
            with open(run_file, encoding="utf-8") as f:
                run = json.load(f)

            signals = detect_failure_signals(run)

            total_cases += 1
            for s in signals:
                signal_counter[s] += 1

        all_results[model] = {
            "total_cases": total_cases,
            "signal_counts": dict(signal_counter),
        }

    return all_results


if __name__ == "__main__":
    results = summarize_from_logs()

    print("\n========== POST-HOC SUMMARY ==========")
    for model_key, stats in results.items():
        print(f"\nMODEL: {model_key}")
        print(f"TOTAL CASES: {stats['total_cases']}")
        print("SIGNAL COUNTS:")
        for signal, count in stats["signal_counts"].items():
            print(f"  {signal}: {count}")

