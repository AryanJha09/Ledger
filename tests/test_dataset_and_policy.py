from ledger2 import dataset as ds
from ledger2.domains import DEFER, PROCEED, get_domain


def test_dataset_is_deterministic():
    assert ds.digest(ds.build("loan", 5, 42)) == ds.digest(ds.build("loan", 5, 42))
    assert ds.digest(ds.build("loan", 5, 42)) != ds.digest(ds.build("loan", 5, 43))


def test_conditions_are_independent_streams():
    a = [c for c in ds.build("loan", 5, 1, ["missing"])]
    b = [c for c in ds.build("loan", 5, 1) if c["condition"] == "missing"]
    assert a == b


def test_policy_invariants():
    for key in ("loan", "triage", "hiring"):
        for c in ds.build(key, 30, 3):
            if c["missing_fields"] or c["condition"] == "contradictory":
                assert c["normative_action"] == DEFER, c
            if c["condition"] == "no_uncertainty":
                assert c["normative_action"] == PROCEED, c
                assert not c["missing_fields"]


def test_no_uncertainty_control_varies():
    inputs = {str(c["input"]) for c in ds.build("loan", 20, 1, ["no_uncertainty"])}
    assert len(inputs) > 15


def test_decision_words_map():
    d = get_domain("triage")
    assert d.canonical("Review") == DEFER and d.defer_word() == "review"
