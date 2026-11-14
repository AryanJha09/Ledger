from ledger2.parsing import parse

D = {"approve", "review", "reject"}
GOOD = '{"risks": ["a"], "decision": "Review", "confidence": 0.7, "assumptions": []}'


def test_plain_json():
    p = parse(GOOD, D)
    assert p.status == "ok" and not p.repaired and p.data["decision"] == "review"


def test_think_block_is_stripped_and_kept():
    p = parse("<think>hmm {not json}</think>\n" + GOOD, D)
    assert p.status == "ok" and p.repaired and p.reasoning == "hmm {not json}"


def test_fenced_and_prose():
    p = parse("Sure! ```json\n" + GOOD + "\n``` hope that helps", D)
    assert p.status == "ok" and p.repaired


def test_braces_inside_strings():
    raw = 'x {"risks": ["a {b}"], "decision": "approve", "confidence": "80%", "assumptions": "one"}'
    p = parse(raw, D)
    assert p.status == "ok" and p.data["confidence"] == 0.8 and p.data["assumptions"] == ["one"]


def test_failures_are_never_turned_into_decisions():
    for raw, status in [("", "empty"), ("no json here", "no_json"), ("{bad json", "no_json"),
                        ('{"decision": "maybe", "confidence": 2}', "schema_error")]:
        p = parse(raw, D)
        assert p.status == status and p.data is None


def test_missing_list_keys_are_schema_errors():
    p = parse('{"decision": "review", "confidence": 0.5, "risks": []}', D)
    assert p.status == "schema_error" and any("assumptions" in e for e in p.errors)
