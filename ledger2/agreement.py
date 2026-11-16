"""Inter-rater agreement and detector validation.

    python -m ledger2.agreement --labels annotation/labels/*.csv --out results/validation

Each label CSV is one annotator's copy of the annotation sheet (see
annotation/GUIDELINES.md) with the ``label`` column filled in. The script
reports Cohen's kappa for every pair, Fleiss' kappa and Krippendorff's alpha
(nominal) across all annotators, builds a majority-vote gold set (ties go to
the adjudication file), and scores the v1 and v2 detectors against it.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from .stats import bootstrap_ci

LABELS = ["benign", "escalated", "degenerate"]


def cohens_kappa(a, b) -> float:
    a, b = list(a), list(b)
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def fleiss_kappa(matrix: np.ndarray) -> float:
    """matrix: items x categories counts, each row summing to the raters per item."""
    m = np.asarray(matrix, dtype=float)
    n_items, _ = m.shape
    r = m.sum(axis=1)[0]
    p_j = m.sum(axis=0) / (n_items * r)
    p_i = ((m * m).sum(axis=1) - r) / (r * (r - 1))
    p_bar, p_e = p_i.mean(), (p_j ** 2).sum()
    return 1.0 if p_e == 1 else float((p_bar - p_e) / (1 - p_e))


def krippendorff_alpha_nominal(units) -> float:
    """units: list of lists of labels (missing values simply omitted)."""
    values = sorted({v for u in units for v in u})
    idx = {v: i for i, v in enumerate(values)}
    o = np.zeros((len(values), len(values)))
    for u in units:
        m = len(u)
        if m < 2:
            continue
        for a, b in itertools.permutations(range(m), 2):
            o[idx[u[a]], idx[u[b]]] += 1.0 / (m - 1)
    n_c = o.sum(axis=1)
    n = n_c.sum()
    if n <= 1:
        return float("nan")
    d_o = (o.sum() - np.trace(o)) / n
    d_e = (n * n - (n_c ** 2).sum()) / (n * (n - 1))
    return 1.0 if d_e == 0 else float(1 - d_o / d_e)


def prf(gold, pred, positive) -> dict:
    tp = sum(g == positive and p == positive for g, p in zip(gold, pred))
    fp = sum(g != positive and p == positive for g, p in zip(gold, pred))
    fn = sum(g == positive and p != positive for g, p in zip(gold, pred))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if prec == prec and rec == rec and prec + rec else float("nan")
    return {"label": positive, "tp": tp, "fp": fp, "fn": fn, "precision": prec, "recall": rec, "f1": f1}


def binary_unsupported(labels):
    return ["unsupported" if x in ("escalated", "degenerate") else "supported" for x in labels]


def run(label_files, key_file: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets = {Path(f).stem: pd.read_csv(f) for f in label_files}
    if len(sheets) < 2:
        raise SystemExit("need at least two annotators")
    names = sorted(sheets)
    base = pd.read_csv(key_file).set_index("item_id")[["v1_label", "v2_label"]]
    lab = pd.DataFrame({n: sheets[n].set_index("item_id")["label"].str.strip().str.lower() for n in names})
    lab = lab.dropna()
    bad = set(lab.values.ravel()) - set(LABELS)
    if bad:
        raise SystemExit(f"unknown labels {bad}; allowed {LABELS}")

    report = {"n_items": int(len(lab)), "annotators": names, "pairwise_cohen": {}}
    for a, b in itertools.combinations(names, 2):
        report["pairwise_cohen"][f"{a}~{b}"] = cohens_kappa(lab[a], lab[b])
    counts = np.array([[sum(row == c) for c in LABELS] for row in lab.values])
    report["fleiss_kappa"] = fleiss_kappa(counts) if len(names) > 2 else None
    report["krippendorff_alpha"] = krippendorff_alpha_nominal([list(r) for r in lab.values])
    report["krippendorff_alpha_binary"] = krippendorff_alpha_nominal(
        [binary_unsupported(list(r)) for r in lab.values])
    # bootstrap CI for alpha over items
    rows = [list(r) for r in lab.values]
    rng = np.random.default_rng(0)
    boots = [krippendorff_alpha_nominal([rows[i] for i in rng.integers(0, len(rows), len(rows))])
             for _ in range(1000)]
    report["krippendorff_alpha_ci"] = [float(np.nanpercentile(boots, 2.5)), float(np.nanpercentile(boots, 97.5))]

    # Majority gold; ties are written out for adjudication.
    gold, ties = {}, []
    for item, r in lab.iterrows():
        c = Counter(r.values).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            ties.append(item)
        else:
            gold[item] = c[0][0]
    adj_path = out_dir / "adjudication_needed.csv"
    lab.loc[ties].to_csv(adj_path)
    adjudicated = out_dir / "adjudicated.csv"
    if adjudicated.exists():
        for _, r in pd.read_csv(adjudicated).iterrows():
            gold[r["item_id"]] = r["label"].strip().lower()
    report["n_gold"] = len(gold)
    report["n_ties"] = len(ties)

    items = [i for i in gold if i in base.index]
    g = [gold[i] for i in items]
    for det in ("v1_label", "v2_label"):
        pred = [base.loc[i, det] for i in items]
        report[det] = {
            "accuracy": float(np.mean([a == b for a, b in zip(g, pred)])),
            "cohen_vs_gold": cohens_kappa(g, pred),
            "per_label": [prf(g, pred, lbl) for lbl in LABELS],
            "unsupported_binary": prf(binary_unsupported(g), binary_unsupported(pred), "unsupported"),
            "accuracy_ci": list(bootstrap_ci([a == b for a, b in zip(g, pred)])),
        }
        # Confusion matrix and misclassified examples for the paper's error analysis.
        cm = pd.crosstab(pd.Series(g, name="gold"), pd.Series(pred, name=det))
        cm.to_csv(out_dir / f"confusion_{det}.csv")
    errors = [{"item_id": i, "gold": gold[i], "v2": base.loc[i, "v2_label"]}
              for i in items if gold[i] != base.loc[i, "v2_label"]]
    pd.DataFrame(errors).to_csv(out_dir / "v2_errors.csv", index=False)
    (out_dir / "agreement.json").write_text(json.dumps(report, indent=2, default=float))
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--labels", nargs="+", required=True)
    p.add_argument("--key", type=Path, default=Path("annotation/sample_key.csv"),
                   help="hidden key with detector labels, written by ledger2.annotation")
    p.add_argument("--out", type=Path, default=Path("results/validation"))
    a = p.parse_args(argv)
    print(json.dumps(run(a.labels, a.key, a.out), indent=2, default=float))


if __name__ == "__main__":
    main()
