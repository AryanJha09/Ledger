import json
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

from agents.real_agent import run_real_agent
from diagnostics.signals import detect_failure_signals
from config.agent_config import AGENT_METADATA


# -----------------------------
# CONFIG (NEGATIVE CONTROL)
# -----------------------------

MODEL_KEY = "mistral_7b"

# Directory containing pre-generated no-uncertainty inputs
BASE_LOG_DIR = Path(__file__).parent / "logs" / "mistral_7b_no_uncertainty"
BASE_LOG_DIR.mkdir(parents=True, exist_ok=True)


def run_no_uncertainty_experiment():
    case_files = sorted(BASE_LOG_DIR.glob("run_*.json"))

    if not case_files:
        raise RuntimeError(
            f"No input files found in {BASE_LOG_DIR}. "
            "Did you generate no-uncertainty cases?"
        )

    print(
        f"[INFO] Running {MODEL_KEY} on {len(case_files)} no-uncertainty cases",
        flush=True
    )

    signal_counter = Counter()
    total_cases = 0

    for run_id, case_file in enumerate(case_files):
        with open(case_file, "r", encoding="utf-8") as f:
            run = json.load(f)

        input_data = run.get("input")
        case_type = run.get("case_type", "no_uncertainty")

        print(
            f"[MODEL {MODEL_KEY}] [RUN {run_id:03d}] Case type: {case_type}",
            flush=True
        )

        # --- Run model ---
        agent_output = run_real_agent(input_data, MODEL_KEY)

        # --- Update run log ---
        run.update({
            "run_id": f"{MODEL_KEY}_no_uncertainty_{run_id:04d}",
            "model": MODEL_KEY,
            "metadata": AGENT_METADATA,
            "agent_output": agent_output,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        # --- Detect behavioral signals ---
        signals = detect_failure_signals(run)
        run["diagnostics"] = signals

        # --- Aggregate statistics ---
        total_cases += 1
        for s in signals:
            signal_counter[s] += 1

        # --- Persist updated run (overwrite) ---
        with open(case_file, "w", encoding="utf-8") as f:
            json.dump(run, f, indent=2)

    print(
        f"[OK] Completed {total_cases} no-uncertainty runs → {BASE_LOG_DIR.resolve()}",
        flush=True
    )

    print("\n========== NEGATIVE CONTROL SUMMARY ==========", flush=True)
    print(f"MODEL: {MODEL_KEY}", flush=True)
    print(f"TOTAL CASES: {total_cases}", flush=True)
    print("SIGNAL COUNTS:", flush=True)
    for signal, count in signal_counter.items():
        print(f"  {signal}: {count}", flush=True)


if __name__ == "__main__":
    run_no_uncertainty_experiment()
