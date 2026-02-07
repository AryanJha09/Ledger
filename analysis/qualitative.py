import json
from pathlib import Path
from analysis.utils import is_tooling_failure

BASE_LOG_DIR = Path("experiments/logs")
CONFIDENCE_THRESHOLD = 0.75  # High-confidence heuristic


def is_high_confidence_uncertainty_case(run: dict) -> bool:
    """
    Selection predicate:
    Model expresses high confidence while relying on assumptions.
    """
    agent_output = run.get("agent_output")
    if not agent_output:
        return False

    confidence = agent_output.get("confidence")
    assumptions = agent_output.get("assumptions")

    if confidence is None or assumptions is None:
        return False

    return confidence >= CONFIDENCE_THRESHOLD and len(assumptions) > 0


def load_first_matching_run(model_dir: Path):
    for run_file in sorted(model_dir.glob("run_*.json")):
        with run_file.open(encoding="utf-8") as f:
            run = json.load(f)

        # --- Step 1C: skip tooling failures ---
        if is_tooling_failure(run):
            continue

        if is_high_confidence_uncertainty_case(run):
            return run_file, run

    return None, None



if __name__ == "__main__":
    for model_dir in sorted(BASE_LOG_DIR.iterdir()):
        if not model_dir.is_dir():
            continue

        run_file, run = load_first_matching_run(model_dir)

        print("\n" + "=" * 60)
        print(f"[MODEL] {model_dir.name}")

        if run is None:
            print("No high-confidence uncertainty case found.")
            continue

        print(f"[QUALITATIVE] Selected run: {run_file.name}")

        # --- Input ---
        print("\n=== INPUT ===")
        print(run.get("input"))

        # --- Model decision ---
        agent_output = run.get("agent_output", {})
        print("\n=== MODEL DECISION ===")
        print({
            "decision": agent_output.get("decision"),
            "confidence": agent_output.get("confidence"),
        })

        # --- Model reasoning / assumptions ---
        print("\n=== MODEL REASONING / ASSUMPTIONS ===")
        assumptions = agent_output.get("assumptions", [])

        if assumptions:
            for idx, assumption in enumerate(assumptions, start=1):
                print(f"{idx}. {assumption}")
        else:
            print("(No explicit assumptions stated)")

        # --- Diagnostics ---
        print("\n=== DIAGNOSTICS ===")
        print(run.get("diagnostics", []))
