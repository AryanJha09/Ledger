"""Domain abstraction shared by all synthetic decision tasks.

A domain defines:
  * the input schema (fields plus the words a model may use to refer to them),
  * a generator for each of the five case conditions,
  * a written normative policy giving the expected action for every case,
  * the warning signs that make "risk rationalization" measurable,
  * the prompt wording.

Every case is generated from an explicit ``numpy.random.Generator`` so a
dataset is fully determined by (domain, seed, n_per_condition).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import numpy as np

CONDITIONS = ["normal", "missing", "contradictory", "stress", "no_uncertainty"]

# Canonical action labels. Each domain maps its own wording onto these three.
PROCEED, DEFER, DECLINE = "proceed", "defer", "decline"


@dataclass(frozen=True)
class FieldSpec:
    name: str
    # Lower-case substrings a model might use when talking about this field.
    lexicon: tuple
    description: str = ""


@dataclass
class Domain:
    key: str
    title: str
    role: str  # e.g. "loan evaluation agent"
    fields: List[FieldSpec]
    decisions: Dict[str, str]  # domain word -> canonical action
    generators: Dict[str, Callable[[np.random.Generator], dict]]
    policy: Callable[[dict, str], str]  # (case, condition) -> canonical action
    warning_signs: Callable[[dict], List[str]]
    # Extra-schema facts: things a model can only "know" by inventing them.
    extra_schema_lexicon: tuple = field(default_factory=tuple)

    @property
    def field_names(self) -> List[str]:
        return [f.name for f in self.fields]

    def canonical(self, decision: Optional[str]) -> Optional[str]:
        if decision is None:
            return None
        return self.decisions.get(str(decision).strip().lower())

    def defer_word(self) -> str:
        return next(k for k, v in self.decisions.items() if v == DEFER)

    def generate(self, condition: str, rng: np.random.Generator) -> dict:
        if condition not in self.generators:
            raise ValueError(f"{self.key}: unknown condition {condition!r}")
        return self.generators[condition](rng)


def blank_fields(case: dict, rng: np.random.Generator, k_min=1, k_max=2) -> dict:
    """Return a copy of ``case`` with k random fields set to None."""
    case = dict(case)
    keys = list(case.keys())
    k = int(rng.integers(k_min, k_max + 1))
    for key in rng.choice(keys, size=k, replace=False):
        case[str(key)] = None
    return case


def maybe(rng: np.random.Generator, value, p_none: float):
    return None if rng.random() < p_none else value
