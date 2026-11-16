import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ledger2 import dataset as ds  # noqa: E402
from ledger2.domains import get_domain  # noqa: E402
from ledger2.parsing import parse  # noqa: E402


def _stub_response(case, rng, style):
    """Test-only stand-in for a model. Never used for results."""
    d = get_domain(case["domain"])
    words = list(d.decisions)
    if style == "think":
        prefix = "<think>let me reason</think>\n"
    elif style == "prose":
        prefix = "Here is my answer:\n```json\n"
    else:
        prefix = ""
    obj = {
        "risks": case["warning_signs"],
        "decision": words[int(rng.integers(0, 3))],
        "confidence": round(float(rng.uniform(0.5, 0.95)), 2),
        "assumptions": (["Income will remain stable"] if case["missing_fields"] else ["Credit score is good"]),
    }
    body = json.dumps(obj)
    return prefix + body + ("\n```" if style == "prose" else "")


@pytest.fixture
def fake_runs(tmp_path):
    rng = np.random.default_rng(0)
    runs_dir = tmp_path / "runs"
    for model, style in [("m_plain", "plain"), ("m_think", "think"), ("m_prose", "prose")]:
        for dom in ("loan", "triage"):
            cases = ds.build(dom, 6, 1)
            path = runs_dir / model / dom / "p1_autonomous.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w") as f:
                for c in cases:
                    for s in range(2):
                        raw = _stub_response(c, rng, style) if rng.random() > 0.1 else "not json at all"
                        p = parse(raw, set(get_domain(dom).decisions))
                        f.write(json.dumps({
                            "run_id": f"{model}|{dom}|p1|{c['case_id']}|s{s}", "model_key": model,
                            "model": {"tag": model}, "domain": dom, "prompt_id": "p1_autonomous",
                            "case_id": c["case_id"], "condition": c["condition"], "input": c["input"],
                            "normative_action": c["normative_action"], "warning_signs": c["warning_signs"],
                            "sample_index": s, "options": {}, "json_mode": False,
                            "generation": {"response": raw}, "parse_status": p.status,
                            "parse_repaired": p.repaired, "parse_errors": p.errors, "output": p.data,
                        }) + "\n")
    return runs_dir
