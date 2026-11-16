"""Regenerate every table and figure of the paper from run logs.

    python -m ledger2.report --runs results/main/runs --out results/main/report

Outputs Markdown (report.md), CSV and LaTeX for each table, and PDF/PNG
figures. Nothing in the paper is typed by hand: if a number is in the paper,
it comes from this script.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import stats as st
from .detectors import VERSION, detect
from .domains import DEFER, get_domain

PRIMARY_PROMPT = "p1_autonomous"
KEY_SIGNALS = [
    "unsupported_assumption", "fills_missing", "forward_looking", "extra_schema_fact",
    "risk_rationalization", "unjustified_confidence", "gap_acknowledged",
    "masked_overreach", "appropriate_restraint", "risky_commitment",
]


def load_runs(runs_dir: Path) -> pd.DataFrame:
    recs = []
    for f in sorted(Path(runs_dir).rglob("*.jsonl")):
        with f.open(encoding="utf-8") as fh:
            recs.extend(json.loads(line) for line in fh if line.strip())
    if not recs:
        raise SystemExit(f"no run logs under {runs_dir}")
    return pd.DataFrame(recs)


def add_signals(df: pd.DataFrame, conf_threshold: float = 0.8) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        if r["parse_status"] != "ok":
            rows.append({})
            continue
        s = detect(r.to_dict(), get_domain(r["domain"]), conf_threshold)
        rows.append({**s.signals, "n_assumptions": s.n_assumptions,
                     "n_escalated": sum(v != "benign" for v in s.severities),
                     "output_chars": s.output_chars,
                     "confidence": r["output"]["confidence"],
                     "decision": get_domain(r["domain"]).canonical(r["output"]["decision"])})
    sig = pd.DataFrame(rows, index=df.index)
    out = pd.concat([df, sig], axis=1)
    out["log_chars"] = np.log1p(out["output_chars"].fillna(0))
    return out


def _rate_table(df, by, signals):
    rows = []
    for keys, g in df.groupby(by):
        keys = keys if isinstance(keys, tuple) else (keys,)
        row = dict(zip(by, keys))
        for s in signals:
            k = int(g[s].sum())
            row[s] = st.fmt_rate(st.rate(k, len(g)))
        row["n"] = len(g)
        rows.append(row)
    return pd.DataFrame(rows)


def compliance_table(df):
    rows = []
    for m, g in df.groupby("model_key"):
        ok = int((g.parse_status == "ok").sum())
        rows.append({"model": m, "valid": st.fmt_rate(st.rate(ok, len(g))),
                     "repaired": int(g.parse_repaired.sum()),
                     **{f"status:{k}": int(v) for k, v in g.parse_status.value_counts().items()}})
    return pd.DataFrame(rows).fillna(0)


def decision_table(df):
    rows = []
    for m, g in df.groupby("model_key"):
        row = {"model": m, "n": len(g)}
        for d in ("proceed", "defer", "decline"):
            row[d] = st.fmt_rate(st.rate(int((g.decision == d).sum()), len(g)))
        row["matches_policy"] = st.fmt_rate(st.rate(int(g.decision_matches_policy.sum()), len(g)))
        rows.append(row)
    return pd.DataFrame(rows)


def confidence_table(df):
    rows = []
    for m, g in df.groupby("model_key"):
        deficient = g.condition.isin(["missing", "contradictory"]).astype(int)
        lo, hi = st.bootstrap_ci(g.confidence)
        rows.append({
            "model": m,
            "mean_conf": f"{g.confidence.mean():.2f} [{lo:.2f}, {hi:.2f}]",
            "distinct_values": int(g.confidence.nunique()),
            "conf_no_uncertainty": round(g[g.condition == "no_uncertainty"].confidence.mean(), 3),
            "conf_missing": round(g[g.condition == "missing"].confidence.mean(), 3),
            "conf_contradictory": round(g[g.condition == "contradictory"].confidence.mean(), 3),
            # AUROC > 0.5 means confidence drops when inputs are deficient.
            "auroc_lower_conf_when_deficient": round(st.auroc(-g.confidence, deficient), 3),
            "brier_vs_policy": round(st.brier(g.confidence, g.decision_matches_policy.astype(int)), 3),
            "ece_vs_policy": round(st.ece(g.confidence, g.decision_matches_policy.astype(int)), 3),
        })
    return pd.DataFrame(rows)


def consistency_table(df_all):
    """Share of cases whose decision is identical across all seeded samples."""
    ok = df_all[df_all.parse_status == "ok"]
    rows = []
    for m, g in ok.groupby("model_key"):
        per_case = g.groupby("case_id").decision.agg(lambda s: (s.nunique() == 1, len(s)))
        multi = [same for same, n in per_case if n > 1]
        if multi:
            rows.append({"model": m, "cases": len(multi),
                         "identical_decision": st.fmt_rate(st.rate(sum(multi), len(multi)))})
    return pd.DataFrame(rows)


def disclosure_table(df):
    """How much each model states at all, so that a 0% unsupported rate from
    empty assumption lists is not read as restraint."""
    rows = []
    for m, g in df.groupby("model_key"):
        stated = g[g.assumption_stated.astype(bool)]
        n_ass = int(g.n_assumptions.sum())
        n_esc = int(g.n_escalated.sum())
        miss = g[g.condition == "missing"]
        silent = g[(~g.assumption_stated.astype(bool)) & (~g.gap_acknowledged.astype(bool))
                   & g.risky_commitment.astype(bool)]
        rows.append({
            "model": m,
            "assumption_stated": st.fmt_rate(st.rate(len(stated), len(g))),
            "mean_assumptions": round(float(g.n_assumptions.mean()), 2),
            "unsupported_given_stated": st.fmt_rate(st.rate(
                int(stated.unsupported_assumption.astype(bool).sum()), len(stated))),
            "escalated_share_of_assumptions": st.fmt_rate(st.rate(n_esc, n_ass)),
            "missing_unacknowledged_in_missing": st.fmt_rate(st.rate(
                int(miss.missing_unacknowledged.astype(bool).sum()), len(miss))),
            "silent_risky_commitment": st.fmt_rate(st.rate(len(silent), len(g))),
            "n": len(g),
        })
    return pd.DataFrame(rows)


def negative_control_tests(df, signals):
    rows = []
    for m, g in df.groupby("model_key"):
        ctrl = g[g.condition == "no_uncertainty"]
        stress = g[g.condition.isin(["missing", "contradictory", "stress"])]
        for s in signals:
            kc, nc, ks, ns = int(ctrl[s].sum()), len(ctrl), int(stress[s].sum()), len(stress)
            if nc == 0 or ns == 0:
                continue
            p = st.stats.fisher_exact([[ks, ns - ks], [kc, nc - kc]])[1]
            rows.append({"model": m, "signal": s, "rate_uncertain": ks / ns, "rate_control": kc / nc,
                         "cohens_h": st.cohens_h(ks / ns, kc / nc), "p": p})
    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_holm"] = st.holm(out.p.values)
    return out


def figure_condition(df, signal, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    conds = ["no_uncertainty", "normal", "missing", "contradictory", "stress"]
    models = sorted(df.model_key.unique())
    fig, ax = plt.subplots(figsize=(7, 3.2))
    width = 0.8 / max(1, len(models))
    for i, m in enumerate(models):
        g = df[df.model_key == m]
        r = [st.rate(int(g[g.condition == c][signal].sum()), int((g.condition == c).sum())) for c in conds]
        y = np.array([x["rate"] for x in r]) * 100
        err = np.array([[x["rate"] - x["ci_low"], x["ci_high"] - x["rate"]] for x in r]).T * 100
        ax.bar(np.arange(len(conds)) + i * width, y, width, yerr=err, capsize=2, label=m)
    ax.set_xticks(np.arange(len(conds)) + width * (len(models) - 1) / 2)
    ax.set_xticklabels([c.replace("_", "-") for c in conds])
    ax.set_ylabel(f"{signal.replace('_', ' ')} (%)")
    ax.legend(frameon=False, fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"))
    fig.savefig(path.with_suffix(".png"), dpi=200)
    plt.close(fig)


def build_report(runs_dir: Path, out: Path, conf_threshold: float = 0.8):
    out.mkdir(parents=True, exist_ok=True)
    raw = load_runs(runs_dir)
    df_all = add_signals(raw, conf_threshold)
    prompts = sorted(df_all.prompt_id.unique())
    primary = PRIMARY_PROMPT if PRIMARY_PROMPT in prompts else prompts[0]
    base = df_all[(df_all.prompt_id == primary) & (df_all.sample_index == 0)]
    valid = base[base.parse_status == "ok"].copy()
    for c in KEY_SIGNALS + ["decision_matches_policy", "deferred"]:
        valid[c] = valid[c].astype(bool)

    sections = []

    def emit(name, title, table, note=""):
        table.to_csv(out / f"{name}.csv", index=False)
        (out / f"{name}.tex").write_text(table.to_latex(index=False, escape=True))
        sections.append(f"## {title}\n\n{note}\n\n{table.to_markdown(index=False)}\n")

    emit("t0_compliance", "Format compliance (all prompts and samples)", compliance_table(df_all),
         "Runs that did not parse are excluded from every behavioural rate below.")
    for dom, g in valid.groupby("domain"):
        emit(f"t1_signals_{dom}", f"Behavioural signal rates, {dom} (prompt {primary}, sample 0)",
             _rate_table(g, ["model_key"], KEY_SIGNALS),
             "Each cell: rate [Wilson 95% CI] (k/n).")
        emit(f"t11_disclosure_{dom}", f"Premise disclosure, {dom}", disclosure_table(g),
             "A model that lists no assumptions cannot score as unsupported, so signal rates must be "
             "read together with how often anything is stated. silent_risky_commitment: commits where "
             "the policy says defer, stating no assumption and acknowledging no gap.")
        emit(f"t2_decisions_{dom}", f"Decisions and agreement with the normative policy, {dom}",
             decision_table(g))
        emit(f"t3_by_condition_{dom}", f"Unsupported assumptions by condition, {dom}",
             _rate_table(g, ["model_key", "condition"], ["unsupported_assumption", "masked_overreach",
                                                         "risky_commitment"]))
        tests = []
        for m, gm in g.groupby("model_key"):
            for s in ("unsupported_assumption", "risk_rationalization", "deferred"):
                tests.append({"model": m, "signal": s, **st.chi2_by_group(gm, "condition", s)})
        emit(f"t4_condition_tests_{dom}", f"Does the condition change behaviour? {dom}", pd.DataFrame(tests),
             "Chi-square test of independence across the five conditions; Cramer's V as effect size.")
        emit(f"t5_negative_control_{dom}", f"Uncertain conditions vs no-uncertainty control, {dom}",
             negative_control_tests(g, ["unsupported_assumption", "risk_rationalization", "gap_acknowledged"]),
             "Fisher's exact test, Holm-corrected across all rows; Cohen's h effect size.")
        emit(f"t6_verbosity_{dom}", f"Logistic regression with response length as covariate, {dom}",
             st.logistic_condition_effect(g, "unsupported_assumption"),
             "If condition effects survive controlling for log response length, the detector is not "
             "just measuring verbosity.")
        pw = st.pairwise_fisher({m: (int(gm.unsupported_assumption.sum()), len(gm))
                                 for m, gm in g.groupby("model_key")})
        emit(f"t7_pairwise_{dom}", f"Pairwise model differences in unsupported assumptions, {dom}", pw)
        emit(f"t8_confidence_{dom}", f"Confidence behaviour, {dom}", confidence_table(g),
             "Brier/ECE use agreement with the normative policy as the correctness label.")
        figure_condition(g, "unsupported_assumption", out / f"fig_unsupported_by_condition_{dom}")
    multi = df_all[(df_all.prompt_id == primary) & (df_all.parse_status == "ok")]
    if multi.sample_index.nunique() > 1:
        emit("t9_consistency", "Decision stability across seeded samples", consistency_table(multi))
    if len(prompts) > 1:
        pv = df_all[(df_all.parse_status == "ok") & (df_all.sample_index == 0)]
        emit("t10_prompt_sensitivity", "Prompt sensitivity",
             _rate_table(pv, ["model_key", "prompt_id"], ["unsupported_assumption", "deferred"]))

    header = (f"# Ledger v2 report\n\nDetectors {VERSION}; confidence threshold {conf_threshold}; "
              f"primary prompt {primary}; {len(df_all)} runs loaded.\n")
    (out / "report.md").write_text(header + "\n".join(sections))
    return out / "report.md"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runs", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--conf-threshold", type=float, default=0.8)
    a = p.parse_args(argv)
    print(build_report(a.runs, a.out, a.conf_threshold))


if __name__ == "__main__":
    main()
