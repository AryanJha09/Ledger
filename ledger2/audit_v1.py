"""Audit of the logs behind the original submission (v1).

    python -m ledger2.audit_v1 --logs experiments/logs --out results/audit_v1

Reports, per model: how many runs actually parsed, the paper's Table II/III
numbers recomputed on valid runs only with Wilson CIs, and how the v1
hedge-word detector compares with the v2 grounded detector on the same text.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd

from diagnostics.assumption_types import classify_assumption as v1_classify
from diagnostics.signals import detect_failure_signals

from . import stats as st
from .detectors import classify_assumption, severity
from .domains import get_domain

PAPER_TABLE_II = {  # as printed in the IC3AI submission
    "mistral_7b": {"assumption_invention": 56, "assumption_escalation": 7, "risk_rationalization": 19,
                   "unjustified_confidence": 7},
    "llama3_8b": {"assumption_invention": 0, "assumption_escalation": 0, "risk_rationalization": 0,
                  "unjustified_confidence": 0},
    "qwen2_5_7b": {"assumption_invention": 3, "assumption_escalation": 2, "risk_rationalization": 3,
                   "unjustified_confidence": 16},
    "phi3_medium": {"assumption_invention": 2, "assumption_escalation": 1, "risk_rationalization": 1,
                    "unjustified_confidence": 2},
    "deepseek_r1_7b": {"assumption_invention": 0, "assumption_escalation": 0, "risk_rationalization": 0,
                       "unjustified_confidence": 0},
}
V1_SIGNALS = ["assumption_invention", "assumption_escalation", "risk_rationalization", "unjustified_confidence"]


def load(logs: Path):
    runs = []
    for d in sorted(p for p in logs.iterdir() if p.is_dir()):
        for f in sorted(d.glob("run_*.json")):
            r = json.loads(f.read_text())
            r["_model_dir"] = d.name
            runs.append(r)
    return runs


def audit(logs: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    runs = load(logs)
    loan = get_domain("loan")
    comp, sig_rows, det_rows = [], [], []
    by_model = {}
    for r in runs:
        by_model.setdefault(r["_model_dir"], []).append(r)
    for m, rs in sorted(by_model.items()):
        failed = [r for r in rs if "meta_error" in r.get("agent_output", {})]
        valid = [r for r in rs if "meta_error" not in r.get("agent_output", {})]
        comp.append({"model": m, "runs": len(rs), "parse_failures": len(failed),
                     "valid": st.fmt_rate(st.rate(len(valid), len(rs))),
                     "conditions": dict(Counter(r["case_type"] for r in rs))})
        row = {"model": m, "valid_n": len(valid)}
        for s in V1_SIGNALS:
            k = sum(s in detect_failure_signals(r) for r in valid)
            row[s] = st.fmt_rate(st.rate(k, len(valid))) if valid else "no valid runs"
            if m in PAPER_TABLE_II:
                row[s + " (paper)"] = f"{PAPER_TABLE_II[m][s]}%"
        sig_rows.append(row)
        for r in valid:
            for a in r["agent_output"].get("assumptions", []):
                tags = classify_assumption(a, loan, r["input"])
                det_rows.append({"model": m, "condition": r["case_type"], "assumption": a,
                                 "v1": v1_classify(a), "v2": severity(tags), "v2_tags": "|".join(tags)})
    comp_df, sig_df, det_df = pd.DataFrame(comp), pd.DataFrame(sig_rows), pd.DataFrame(det_rows)
    comp_df.to_csv(out / "compliance.csv", index=False)
    sig_df.to_csv(out / "table2_recomputed.csv", index=False)
    det_df.to_csv(out / "assumptions_v1_vs_v2.csv", index=False)
    cross = pd.crosstab(det_df.v1, det_df.v2) if not det_df.empty else pd.DataFrame()
    cross.to_csv(out / "v1_vs_v2_crosstab.csv")

    lines = ["# Audit of the v1 submission logs", ""]
    lines += ["## Format compliance", "",
              "A failed parse was replaced by `review / 0.5 / []` and counted as behaviour in the paper.", "",
              comp_df.to_markdown(index=False), ""]
    lines += ["## Table II recomputed on valid runs only (Wilson 95% CI)", "", sig_df.to_markdown(index=False), ""]
    lines += ["## v1 hedge-word detector vs v2 grounded detector (same assumptions)", "",
              cross.to_markdown(), "",
              "Examples where they disagree:", ""]
    if not det_df.empty:
        dis = det_df[det_df.v1 != det_df.v2].head(12)
        lines += [dis[["model", "condition", "assumption", "v1", "v2", "v2_tags"]].to_markdown(index=False)]
    (out / "audit.md").write_text("\n".join(lines) + "\n")
    return out / "audit.md"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--logs", type=Path, default=Path("experiments/logs"))
    p.add_argument("--out", type=Path, default=Path("results/audit_v1"))
    a = p.parse_args(argv)
    print(audit(a.logs, a.out))


if __name__ == "__main__":
    main()
