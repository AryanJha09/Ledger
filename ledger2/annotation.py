"""Build a blinded, stratified annotation sample from run logs.

    python -m ledger2.annotation --runs results/main/runs --n 300 --out annotation

Writes
  annotation/sheet_template.csv  one copy per annotator; fill the `label` column
  annotation/sample_key.csv      hidden: model, condition, v1 and v2 labels
Annotators never see the model name or any detector output. Items are
stratified by condition x v2 severity so that rare categories are present.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from diagnostics.assumption_types import classify_assumption as v1_classify

from .domains import get_domain
from .detectors import classify_assumption, severity
from .report import load_runs


def build(runs_dir: Path, n: int, seed: int = 7) -> tuple:
    df = load_runs(runs_dir)
    df = df[(df.parse_status == "ok") & (df.sample_index == 0)]
    rows = []
    for _, r in df.iterrows():
        d = get_domain(r["domain"])
        for j, a in enumerate(r["output"]["assumptions"]):
            tags = classify_assumption(a, d, r["input"])
            rows.append({
                "item_key": f"{r['run_id']}#{j}",
                "model_key": r["model_key"], "domain": r["domain"], "condition": r["condition"],
                "input": json.dumps(r["input"]), "decision": r["output"]["decision"],
                "assumption": a, "v1_label": v1_classify(a), "v2_label": severity(tags),
                "v2_tags": "|".join(tags),
            })
    items = pd.DataFrame(rows).drop_duplicates(subset=["domain", "input", "assumption"])
    rng = np.random.default_rng(seed)
    strata = items.groupby(["condition", "v2_label"])
    per = max(1, n // max(1, strata.ngroups))
    picked = pd.concat([g.sample(min(len(g), per), random_state=int(rng.integers(1e9))) for _, g in strata])
    if len(picked) < n:  # top up proportionally from the remainder
        rest = items.drop(picked.index)
        picked = pd.concat([picked, rest.sample(min(len(rest), n - len(picked)), random_state=seed)])
    picked = picked.sample(frac=1, random_state=seed).reset_index(drop=True)
    picked.insert(0, "item_id", [f"A{i:04d}" for i in range(len(picked))])
    sheet = picked[["item_id", "domain", "input", "decision", "assumption"]].assign(label="", note="")
    key = picked[["item_id", "item_key", "model_key", "domain", "condition", "v1_label", "v2_label", "v2_tags"]]
    return sheet, key


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runs", type=Path, required=True)
    p.add_argument("--n", type=int, default=300)
    p.add_argument("--out", type=Path, default=Path("annotation"))
    a = p.parse_args(argv)
    sheet, key = build(a.runs, a.n)
    a.out.mkdir(parents=True, exist_ok=True)
    sheet.to_csv(a.out / "sheet_template.csv", index=False)
    key.to_csv(a.out / "sample_key.csv", index=False)
    print(f"{len(sheet)} items -> {a.out}/sheet_template.csv (key: sample_key.csv)")


if __name__ == "__main__":
    main()
