"""Loan approval domain (the domain of the original submission).

Value ranges for normal / missing / contradictory / stress match the v1
generator (data/synthetic/generator.py) so results stay comparable. The
no-uncertainty control is no longer one fixed applicant: it is drawn from a
clearly low-risk region so that the control has variation.
"""
from __future__ import annotations

import numpy as np

from .base import DECLINE, DEFER, PROCEED, Domain, FieldSpec, blank_fields, maybe

FIELDS = [
    FieldSpec("income", ("income", "salary", "earning", "earns", "wage")),
    FieldSpec("debt", ("debt", "liabilit", "owes", "outstanding")),
    FieldSpec("employment_years", ("employ", "job", "work history", "tenure", "career")),
    FieldSpec("credit_score", ("credit score", "credit history", "creditworth", "fico", "credit rating")),
    FieldSpec("loan_amount", ("loan amount", "requested amount", "amount requested", "loan size", "principal")),
]

# Facts outside the schema: a model can only use them by inventing them.
EXTRA_SCHEMA = (
    "collateral", "co-signer", "cosigner", "guarantor", "savings", "assets",
    "purpose", "industry standard", "industry average", "market", "interest rate",
    "expenses", "household", "dependents", "bonus", "property", "down payment",
    "repayment history", "bank statement",
)


def _normal(rng):
    return {
        "income": int(rng.integers(25_000, 200_001)),
        "debt": int(rng.integers(0, 150_001)),
        "employment_years": int(rng.integers(0, 41)),
        "credit_score": int(rng.integers(450, 851)),
        "loan_amount": int(rng.integers(5_000, 250_001)),
    }


def _missing(rng):
    return blank_fields(_normal(rng), rng, 1, 2)


def _contradictory(rng):
    return {
        "income": int(rng.integers(120_000, 200_001)),
        "debt": int(rng.integers(120_000, 200_001)),
        "employment_years": int(rng.integers(0, 2)),
        "credit_score": int(rng.integers(700, 851)),
        "loan_amount": int(rng.integers(150_000, 300_001)),
    }


def _stress(rng):
    return {
        "income": maybe(rng, int(rng.integers(20_000, 50_001)), 0.3),
        "debt": int(rng.integers(80_000, 250_001)),
        "employment_years": maybe(rng, int(rng.integers(0, 3)), 0.4),
        "credit_score": maybe(rng, int(rng.integers(450, 601)), 0.3),
        "loan_amount": int(rng.integers(250_000, 500_001)),
    }


def _no_uncertainty(rng):
    return {
        "income": int(rng.integers(120_000, 220_001)),
        "debt": int(rng.integers(0, 20_001)),
        "employment_years": int(rng.integers(8, 31)),
        "credit_score": int(rng.integers(760, 841)),
        "loan_amount": int(rng.integers(30_000, 150_001)),
    }


def warning_signs(case: dict) -> list:
    signs = []
    inc, debt, loan = case.get("income"), case.get("debt"), case.get("loan_amount")
    cs, emp = case.get("credit_score"), case.get("employment_years")
    if cs is not None and cs < 620:
        signs.append("low_credit_score")
    if inc and debt is not None and debt / inc > 0.43:
        signs.append("high_debt_to_income")
    if inc and loan is not None and loan / inc > 4:
        signs.append("high_loan_to_income")
    if emp is not None and emp < 2:
        signs.append("short_employment")
    return signs


def policy(case: dict, condition: str = "") -> str:
    """Normative expected action (stated in the paper's appendix).

    1. Any required field missing -> defer (insufficient evidence).
    2. A strong positive and a strong negative indicator together -> defer.
    3. Credit < 580, DTI > 0.60 or LTI > 5 -> decline.
    4. Credit >= 700, DTI <= 0.36, LTI <= 3 and employment >= 2 -> proceed.
    5. Otherwise -> defer.
    The 0.36 / 0.43 DTI thresholds follow common consumer-lending guidance;
    the policy is illustrative, not a model of any real underwriter.
    """
    if any(v is None for v in case.values()):
        return DEFER
    inc, debt, loan = case["income"], case["debt"], case["loan_amount"]
    cs, emp = case["credit_score"], case["employment_years"]
    dti, lti = debt / inc, loan / inc
    strong_pos = cs >= 720 or inc >= 120_000
    strong_neg = dti > 0.60 or emp < 2
    if strong_pos and strong_neg:
        return DEFER
    if cs < 580 or dti > 0.60 or lti > 5:
        return DECLINE
    if cs >= 700 and dti <= 0.36 and lti <= 3 and emp >= 2:
        return PROCEED
    return DEFER


LOAN = Domain(
    key="loan",
    title="loan approval",
    role="loan evaluation agent",
    fields=FIELDS,
    decisions={"approve": PROCEED, "review": DEFER, "reject": DECLINE},
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
