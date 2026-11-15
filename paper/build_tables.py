"""Compact paper tables generated from results/main/report/*.csv (no hand-copied numbers).

    python paper/build_tables.py
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REP = ROOT / "results" / "main" / "report"
OUT = Path(__file__).resolve().parent / "generated"
NAMES = {"mistral_7b": "Mistral", "llama3_8b": "LLaMA-3", "qwen2_5_7b": "Qwen2.5",
         "phi3_medium": "Phi-3", "deepseek_r1_7b": "DS-R1"}
ORDER = list(NAMES)
DOMAINS = ["loan", "triage", "hiring"]


MIN_N = 10  # rates on fewer than 10 runs are shown as "--"


def pct(cell):
    """'76% [70, 81] (190/250)' -> '76'; 'n/a' or n < MIN_N -> '--'."""
    m = re.match(r"\s*(\d+)%.*\((\d+)/(\d+)\)", str(cell))
    return m.group(1) if m and int(m.group(3)) >= MIN_N else "--"


def main_table():
    cols = [("assumption_stated", "St", "t11"), ("unsupported_assumption", "Un", "t1"),
            ("unsupported_given_stated", r"Un$\mid$St", "t11"), ("defer", "Df", "t2"),
            ("matches_policy", "Pol", "t2"), ("masked_overreach", "MO", "t1"),
            ("risky_commitment", "RC", "t1"), ("silent_risky_commitment", "SRC", "t11")]
    lines = [r"\begin{tabular}{ll" + "r" * len(cols) + "}", r"\toprule",
             "Dom. & Model & " + " & ".join(c[1] for c in cols) + r" \\", r"\midrule"]
    for d in DOMAINS:
        t = {"t1": pd.read_csv(REP / f"t1_signals_{d}.csv").set_index("model_key"),
             "t2": pd.read_csv(REP / f"t2_decisions_{d}.csv").set_index("model"),
             "t11": pd.read_csv(REP / f"t11_disclosure_{d}.csv").set_index("model")}
        for i, m in enumerate(ORDER):
            vals = [pct(t[src].loc[m, c]) for c, _, src in cols]
            lines.append((d.capitalize() if i == 0 else "") + f" & {NAMES[m]} & " + " & ".join(vals) + r" \\")
        lines.append(r"\midrule" if d != DOMAINS[-1] else r"\bottomrule")
    lines.append(r"\end{tabular}")
    (OUT / "tab_main.tex").write_text("\n".join(lines) + "\n")


def confidence_table():
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r"Model & \multicolumn{3}{c}{AUROC (deficient $\Rightarrow$ lower conf.)} & \multicolumn{3}{c}{Distinct values} \\",
             r" & Loan & Triage & Hiring & Loan & Triage & Hiring \\", r"\midrule"]
    t = {d: pd.read_csv(REP / f"t8_confidence_{d}.csv").set_index("model") for d in DOMAINS}
    for m in ORDER:
        a = [f"{t[d].loc[m, 'auroc_lower_conf_when_deficient']:.2f}" for d in DOMAINS]
        n = [str(int(t[d].loc[m, "distinct_values"])) for d in DOMAINS]
        lines.append(f"{NAMES[m]} & " + " & ".join(a + n) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "tab_confidence.tex").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    main_table()
    confidence_table()
    print("wrote", *sorted(p.name for p in OUT.iterdir()))
