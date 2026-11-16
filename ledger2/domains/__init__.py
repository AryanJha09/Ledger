from .base import CONDITIONS, DECLINE, DEFER, PROCEED, Domain  # noqa: F401
from .hiring import HIRING
from .loan import LOAN
from .triage import TRIAGE

DOMAINS = {d.key: d for d in (LOAN, TRIAGE, HIRING)}


def get_domain(key: str) -> Domain:
    try:
        return DOMAINS[key]
    except KeyError as e:
        raise ValueError(f"Unknown domain {key!r}; choose from {sorted(DOMAINS)}") from e
