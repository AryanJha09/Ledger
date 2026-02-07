import json
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

from agents.null_agent import run_null_agent
from agents.real_agent import run_real_agent, MODELS
from data.synthetic.generator import generate_dataset
from diagnostics.signals import detect_failure_signals
from config.agent_config import AGENT_METADATA


# ----------------------------
# Paths and constants
# ----------------------------
BASE_LOG_DIR = Path(__file__).parent / "logs"
BASE_LOG_DIR.mkdir(exist_ok=True)

NULL_AGENT_KEY = "null_agent"
NULL_AGENT_DIR = BASE_LOG_DIR / NULL_AGENT_KEY
NULL_AGENT_DIR.mkdir(exist_ok=True)


# ----------------------------
# Main experiment runner
# ----------------------------
def run_batch_experiment(n_per_type=10):
    dataset = generate_dataset(n_per_type)

    # Create per-model log directories
    for model_key in MODELS.keys():
        (BASE_LOG_DIR / model_key).mkdir(exist_ok=True)

    print(f"[INFO] Starting experiment with {len(dataset)} cases per agent", flush=True)

    all_results = {}

    # ======================================================
    # Run REAL MODELS
    # ======================================================
    for model_key in MODELS.keys():
        print(f"\n[MODEL] Running experiments for: {model_key}", flush=True)

        model_log_dir = BASE_LOG_DIR / model_key
        signal_counter = Counter()
        total_cases = 0

        for run_id, item in enumerate(dataset):
            case_type = item["type"]
            input_data = item["data"]

            print(
                f"[MODEL {model_key}] [RUN {run_id:03d}] Case type: {case_type}",
                flush=True
            )

            agent_output = run_real_agent(input_data, model_key)

            run_log = {
                "run_id": f"{model_key}_{run_id:04d}",
                "model": model_key,
                "metadata": AGENT_METADATA,
                "case_type": case_type,
                "input": input_data,
                "agent_output": agent_output,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            signals = detect_failure_signals(run_log)
            run_log["diagnostics"] = signals

            total_cases += 1
            for s in signals:
                signal_counter[s] += 1

            with open(model_log_dir / f"run_{run_id:04d}.json", "w") as f:
                json.dump(run_log, f, indent=2)

        print(
            f"[OK] Logged {total_cases} runs for {model_key} → {model_log_dir.resolve()}",
            flush=True
        )

        all_results[model_key] = {
            "total_cases": total_cases,
            "signal_counts": dict(signal_counter),
        }

    # ======================================================
    # Run NULL AGENT (epistemic baseline)
    # ======================================================
    print(f"\n[MODEL] Running experiments for: {NULL_AGENT_KEY}", flush=True)

    signal_counter = Counter()
    total_cases = 0

    for run_id, item in enumerate(dataset):
        case_type = item["type"]
        input_data = item["data"]

        print(
            f"[MODEL {NULL_AGENT_KEY}] [RUN {run_id:03d}] Case type: {case_type}",
            flush=True
        )

        agent_output = run_null_agent(input_data)

        run_log = {
            "run_id": f"{NULL_AGENT_KEY}_{run_id:04d}",
            "model": NULL_AGENT_KEY,
            "metadata": AGENT_METADATA,
            "case_type": case_type,
            "input": input_data,
            "agent_output": agent_output,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        signals = detect_failure_signals(run_log)
        run_log["diagnostics"] = signals

        total_cases += 1
        for s in signals:
            signal_counter[s] += 1

        with open(NULL_AGENT_DIR / f"run_{run_id:04d}.json", "w") as f:
            json.dump(run_log, f, indent=2)

    print(
        f"[OK] Logged {total_cases} runs for {NULL_AGENT_KEY} → {NULL_AGENT_DIR.resolve()}",
        flush=True
    )

    all_results[NULL_AGENT_KEY] = {
        "total_cases": total_cases,
        "signal_counts": dict(signal_counter),
    }

    return all_results


# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    results = run_batch_experiment(n_per_type=25)

    print("\n========== SUMMARY ==========", flush=True)
    for model_key, stats in results.items():
        print(f"\nMODEL: {model_key}", flush=True)
        print(f"TOTAL CASES: {stats['total_cases']}", flush=True)
        print("SIGNAL COUNTS:", flush=True)
        for signal, count in stats["signal_counts"].items():
            print(f"  {signal}: {count}", flush=True)
