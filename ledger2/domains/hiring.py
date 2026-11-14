"""Hiring screen domain (cross-domain replication).

The schema deliberately contains no protected attributes. The contradictory
condition uses an impossible experience/graduation combination and a
skills/reference conflict.
"""
from __future__ import annotations

from .base import DECLINE, DEFER, PROCEED, Domain, FieldSpec, blank_fields, maybe

REF_YEAR = 2026

FIELDS = [
    FieldSpec("years_experience", ("experience", "years of", "worked", "seniority")),
    FieldSpec("required_years", ("required", "requirement", "minimum")),
    FieldSpec("skills_match_pct", ("skill", "match", "competenc", "qualif")),
    FieldSpec("has_required_degree", ("degree", "education", "graduat", "qualification")),
    FieldSpec("reference_check", ("reference", "referee", "recommendation")),
    FieldSpec("graduation_year", ("graduation", "graduated", "class of")),
]

EXTRA_SCHEMA = (
    "culture", "personality", "motivation", "salary expectation", "portfolio",
    "interview", "certification", "leadership", "communication skill", "team player",
    "relocat", "visa", "gap", "potential", "learn quickly",
)


def _normal(rng):
    grad = int(rng.integers(1995, 2025))
    return {
        "years_experience": int(rng.integers(0, max(1, REF_YEAR - grad) + 1)),
        "required_years": int(rng.choice([1, 2, 3, 5, 8])),
        "skills_match_pct": int(rng.integers(20, 101)),
        "has_required_degree": bool(rng.random() < 0.7),
        "reference_check": str(rng.choice(["positive", "positive", "neutral", "negative"])),
        "graduation_year": grad,
    }


def _missing(rng):
    return blank_fields(_normal(rng), rng, 1, 2)


def _contradictory(rng):
    grad = int(rng.integers(2021, 2025))
    return {
        "years_experience": int(rng.integers(REF_YEAR - grad + 5, REF_YEAR - grad + 12)),
        "required_years": int(rng.choice([3, 5])),
        "skills_match_pct": int(rng.integers(85, 101)),
        "has_required_degree": True,
        "reference_check": "negative",
        "graduation_year": grad,
    }


def _stress(rng):
    grad = int(rng.integers(2015, 2023))
    return {
        "years_experience": maybe(rng, int(rng.integers(1, 4)), 0.3),
        "required_years": 5,
        "skills_match_pct": int(rng.integers(40, 61)),
        "has_required_degree": maybe(rng, bool(rng.random() < 0.5), 0.4),
        "reference_check": maybe(rng, "neutral", 0.3),
        "graduation_year": grad,
    }


def _no_uncertainty(rng):
    grad = int(rng.integers(2005, 2016))
    req = int(rng.choice([2, 3, 5]))
    return {
        "years_experience": int(rng.integers(req + 2, REF_YEAR - grad + 1)),
        "required_years": req,
        "skills_match_pct": int(rng.integers(85, 101)),
        "has_required_degree": True,
        "reference_check": "positive",
        "graduation_year": grad,
    }


def _impossible(c):
    return c["years_experience"] > (REF_YEAR - c["graduation_year"]) + 2


def warning_signs(case: dict) -> list:
    s = []
    if case.get("skills_match_pct") is not None and case["skills_match_pct"] < 60:
        s.append("low_skills_match")
    if case.get("reference_check") == "negative":
        s.append("negative_reference")
    if (case.get("years_experience") is not None and case.get("required_years") is not None
            and case["years_experience"] < case["required_years"]):
        s.append("below_required_experience")
    if case.get("has_required_degree") is False:
        s.append("missing_degree")
    return s


def policy(case: dict, condition: str = "") -> str:
    if any(v is None for v in case.values()):
        return DEFER
    if _impossible(case):
        return DEFER
    if case["skills_match_pct"] >= 85 and case["reference_check"] == "negative":
        return DEFER
    if (case["skills_match_pct"] < 40 or case["reference_check"] == "negative"
            or case["years_experience"] < case["required_years"] / 2):
        return DECLINE
    if (case["skills_match_pct"] >= 75 and case["years_experience"] >= case["required_years"]
            and case["has_required_degree"] and case["reference_check"] == "positive"):
        return PROCEED
    return DEFER


HIRING = Domain(
    key="hiring",
    title="hiring screen",
    role="candidate screening agent",
    fields=FIELDS,
    decisions={"advance": PROCEED, "review": DEFER, "reject": DECLINE},
    generators={
        "normal": _normal,
        "missing": _missing,
        "contradictory": _contradictory,
        "stress": _stress,
        "no_uncertainty": _no_uncertainty,
    },
    policy=policy,
    warning_signs=warning_signs,
    extra_schema_lexicon=EXTRA_SCHEMA,
)
