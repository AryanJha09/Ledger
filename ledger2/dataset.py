"""Seeded, versioned dataset generation.

    python -m ledger2.dataset --domain loan --n 50 --seed 20261114 --out data/v2/loan.jsonl

Each line holds one case with its condition, normative action and warning
signs. A SHA-256 over the canonical JSON of all cases is printed and stored in
a sidecar ``.sha256`` file so the paper can quote the exact dataset hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .domains import CONDITIONS, get_domain


def build(domain_key: str, n_per_condition: int, seed: int, conditions=None):
    domain = get_domain(domain_key)
    conditions = conditions or CONDITIONS
    # One child stream per condition: adding a condition never changes others.
    ss = np.random.SeedSequence([seed, sum(map(ord, domain_key))])
    children = dict(zip(CONDITIONS, ss.spawn(len(CONDITIONS))))
    cases = []
    for cond in conditions:
        rng = np.random.default_rng(children[cond])
        for i in range(n_per_condition):
            x = domain.generate(cond, rng)
            cases.append({
                "case_id": f"{domain_key}-{cond}-{i:03d}",
                "domain": domain_key,
                "condition": cond,
                "input": x,
                "missing_fields": [k for k, v in x.items() if v is None],
                "normative_action": domain.policy(x, cond),
                "warning_signs": domain.warning_signs(x),
            })
    return cases


def digest(cases) -> str:
    blob = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def write(cases, out: Path) -> str:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, sort_keys=True) + "\n")
    h = digest(cases)
    out.with_suffix(out.suffix + ".sha256").write_text(h + "\n")
    return h


def load(path: Path):
    with Path(path).open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--domain", required=True)
    p.add_argument("--n", type=int, default=50, help="cases per condition")
    p.add_argument("--seed", type=int, default=20261114)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args(argv)
    cases = build(a.domain, a.n, a.seed)
    h = write(cases, a.out)
    print(f"wrote {len(cases)} cases to {a.out} sha256={h}")


if __name__ == "__main__":
    main()
