"""Robust parsing of model output, with an explicit status for every run.

The v1 pipeline called ``json.loads`` on the raw text and, on failure,
substituted ``review / 0.5 / []``. Reasoning models (DeepSeek-R1) emit a
``<think>`` block first and other models wrap JSON in prose or code fences,
so most of their runs became that substitute. Here a failed parse is never
turned into a decision: it is recorded as ``status != "ok"`` and excluded
from behavioural rates, and format compliance is reported separately.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


@dataclass
class Parsed:
    status: str  # ok | no_json | invalid_json | schema_error | empty
    repaired: bool = False  # True if anything beyond json.loads(raw) was needed
    data: Optional[dict] = None
    errors: list = field(default_factory=list)
    reasoning: Optional[str] = None  # text of a stripped <think> block


def _first_object(text: str) -> Optional[str]:
    """Return the first balanced {...} substring, respecting JSON strings."""
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        start = text.find("{", start + 1)
    return None


def _coerce_conf(v: Any):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().rstrip("%")
        try:
            f = float(s)
        except ValueError:
            return None
        return f / 100 if v.strip().endswith("%") else f
    return None


def _as_str_list(v: Any) -> Optional[list]:
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v.strip() else []
    if isinstance(v, list):
        out = []
        for item in v:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):  # e.g. {"assumption": "..."}
                out.append("; ".join(str(x) for x in item.values()))
            else:
                out.append(str(item))
        return out
    return None


def parse(raw: Optional[str], allowed_decisions) -> Parsed:
    if raw is None or not raw.strip():
        return Parsed(status="empty")
    text = raw.strip()
    reasoning = None
    m = THINK_RE.search(text)
    if m:
        reasoning = m.group(0)[7:-8].strip()
    body = THINK_RE.sub("", text).strip()
    repaired = body != text

    obj = None
    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        repaired = True
        fence = FENCE_RE.search(body)
        candidate = _first_object(fence.group(1) if fence else body)
        if candidate is None:
            return Parsed(status="no_json", repaired=True, reasoning=reasoning)
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError as e:
            return Parsed(status="invalid_json", repaired=True, errors=[str(e)], reasoning=reasoning)

    if not isinstance(obj, dict):
        return Parsed(status="schema_error", repaired=repaired, errors=["top level is not an object"],
                      reasoning=reasoning)

    errors = []
    decision = obj.get("decision")
    decision = decision.strip().lower() if isinstance(decision, str) else None
    if decision not in allowed_decisions:
        errors.append(f"decision {obj.get('decision')!r} not in {sorted(allowed_decisions)}")
    conf = _coerce_conf(obj.get("confidence"))
    if conf is None or not (0.0 <= conf <= 1.0):
        errors.append(f"confidence {obj.get('confidence')!r} not a number in [0, 1]")
    risks = _as_str_list(obj.get("risks"))
    assumptions = _as_str_list(obj.get("assumptions"))
    if risks is None:
        errors.append("risks is not a list")
    if assumptions is None:
        errors.append("assumptions is not a list")
    if errors:
        return Parsed(status="schema_error", repaired=repaired, errors=errors, reasoning=reasoning)

    return Parsed(
        status="ok",
        repaired=repaired,
        data={"decision": decision, "confidence": conf, "risks": risks, "assumptions": assumptions},
        reasoning=reasoning,
    )
