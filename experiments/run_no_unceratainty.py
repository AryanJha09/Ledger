import json
from pathlib import Path
from data.synthetic.generator import generate_no_uncertainty_case

OUT_DIR = Path("experiments/logs/mistral_7b_no_uncertainty")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for i in range(20):
    case = generate_no_uncertainty_case()
    with open(OUT_DIR / f"run_{i:04d}.json", "w") as f:
        json.dump({
            "case_type": "no_uncertainty",
            "input": case
        }, f, indent=2)

print("Generated 20 no-uncertainty cases.")
