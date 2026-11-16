"""Statistics used in the paper: intervals, tests, effect sizes, models.

All rates are reported as k/n with a Wilson 95% interval. Pairwise model
comparisons use Fisher's exact test with Holm correction and Cohen's h.
Condition effects use a logistic regression with response length as a
covariate (the verbosity control asked for by Reviewer 1, point 11).
"""
from __future__ import annotations

import itertools
import math
from typing import Dict, Sequence

import numpy as np
import pandas as pd
from scipy import stats


def wilson(k: int, n: int, z: float = 1.959964) -> tuple:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def rate(k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"k": int(k), "n": int(n), "rate": (k / n) if n else math.nan, "ci_low": lo, "ci_high": hi}


def fmt_rate(r: dict, digits: int = 0) -> str:
    if not r["n"]:
        return "n/a"
    f = f"{{:.{digits}f}}"
    return (f"{f.format(100 * r['rate'])}% [{f.format(100 * r['ci_low'])}, "
            f"{f.format(100 * r['ci_high'])}] ({r['k']}/{r['n']})")


def cohens_h(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def holm(pvals: Sequence[float]) -> np.ndarray:
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adj[idx] = min(1.0, running)
    return adj


def pairwise_fisher(counts: Dict[str, tuple]) -> pd.DataFrame:
    """counts: group -> (k, n). Returns all pairs with p, Holm-p and Cohen's h."""
    rows = []
    for a, b in itertools.combinations(sorted(counts), 2):
        (ka, na), (kb, nb) = counts[a], counts[b]
        if na == 0 or nb == 0:
            continue
        _, p = stats.fisher_exact([[ka, na - ka], [kb, nb - kb]])
        rows.append({"a": a, "b": b, "rate_a": ka / na, "rate_b": kb / nb,
                     "cohens_h": cohens_h(ka / na, kb / nb), "p": p})
    df = pd.DataFrame(rows)
    if not df.empty:
        df["p_holm"] = holm(df["p"].values)
    return df


def chi2_by_group(df: pd.DataFrame, group: str, outcome: str) -> dict:
    """Chi-square test of independence plus Cramer's V (falls back to Fisher for 2x2)."""
    table = pd.crosstab(df[group], df[outcome].astype(bool))
    if table.shape[1] < 2 or table.shape[0] < 2:
        return {"test": "none", "p": math.nan, "cramers_v": 0.0}
    if table.shape == (2, 2):
        _, p = stats.fisher_exact(table.values)
        chi2 = stats.chi2_contingency(table.values, correction=False)[0]
        test = "fisher"
    else:
        chi2, p, _, _ = stats.chi2_contingency(table.values)
        test = "chi2"
    n = table.values.sum()
    v = math.sqrt(chi2 / (n * (min(table.shape) - 1))) if n else math.nan
    return {"test": test, "p": float(p), "cramers_v": float(v), "dof": int((table.shape[0] - 1) * (table.shape[1] - 1))}


def bootstrap_ci(values: Sequence[float], fn=np.mean, n_boot: int = 5000, seed: int = 0) -> tuple:
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return (math.nan, math.nan)
    rng = np.random.default_rng(seed)
    boots = [fn(rng.choice(x, size=len(x), replace=True)) for _ in range(n_boot)]
    return (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))


def logistic_condition_effect(df: pd.DataFrame, outcome: str, covariates=("log_chars",)) -> pd.DataFrame:
    """Logit(outcome) ~ C(condition, ref=no_uncertainty) + covariates, per model.

    Returns odds ratios with 95% CIs. Separation (a cell with 0 or 100%) is
    common at these sample sizes; then a Firth-free fallback reports NaN and
    the exact tests above carry the inference.
    """
    import statsmodels.formula.api as smf

    rows = []
    for model, g in df.groupby("model_key"):
        g = g.copy()
        g["y"] = g[outcome].astype(int)
        if g["y"].nunique() < 2:
            continue
        cov = " + ".join(covariates)
        formula = f"y ~ C(condition, Treatment(reference='no_uncertainty')) + {cov}"
        try:
            fit = smf.logit(formula, data=g).fit(disp=False, maxiter=200)
            ci = fit.conf_int()
            for term in fit.params.index:
                if term == "Intercept":
                    continue
                rows.append({"model_key": model, "term": term, "odds_ratio": math.exp(fit.params[term]),
                             "or_low": math.exp(ci.loc[term, 0]), "or_high": math.exp(ci.loc[term, 1]),
                             "p": float(fit.pvalues[term])})
        except Exception as e:  # perfect separation etc.
            rows.append({"model_key": model, "term": "fit_failed", "odds_ratio": math.nan,
                         "or_low": math.nan, "or_high": math.nan, "p": math.nan, "error": str(e)[:120]})
    return pd.DataFrame(rows)


def auroc(scores: Sequence[float], labels: Sequence[int]) -> float:
    """Probability that a random positive scores higher than a random negative (ties = 0.5)."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    u = stats.mannwhitneyu(pos, neg, alternative="two-sided").statistic
    return float(u / (len(pos) * len(neg)))


def brier(probs: Sequence[float], labels: Sequence[int]) -> float:
    p = np.asarray(probs, dtype=float)
    y = np.asarray(labels, dtype=float)
    return float(np.mean((p - y) ** 2)) if len(p) else math.nan


def ece(probs: Sequence[float], labels: Sequence[int], n_bins: int = 10) -> float:
    p = np.asarray(probs, dtype=float)
    y = np.asarray(labels, dtype=float)
    if len(p) == 0:
        return math.nan
    bins = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(p, bins[1:-1]), 0, n_bins - 1)
    total = 0.0
    for b in range(n_bins):
        m = idx == b
        if m.any():
            total += m.mean() * abs(p[m].mean() - y[m].mean())
    return float(total)
