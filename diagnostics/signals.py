from diagnostics.assumption_types import classify_assumptions

def detect_failure_signals(run):
    """
    Inspects a single model decision and flags
    epistemically relevant behavior under uncertainty.
    """

    signals = []

    input_data = run.get("input", {})
    agent_output = run.get("agent_output", {})

    decision = agent_output.get("decision")
    confidence = agent_output.get("confidence", 0.0)
    assumptions = agent_output.get("assumptions", [])

    # -----------------------------------------
    # Signal 1: Unjustified confidence
    # -----------------------------------------
    missing_fields = [
        k for k, v in input_data.items()
        if v is None
    ]

    if confidence >= 0.8 and missing_fields:
        signals.append("unjustified_confidence")

    # -----------------------------------------
    # Signal 2: Assumption invention
    # -----------------------------------------
    if assumptions:
        signals.append("assumption_invention")

    # -----------------------------------------
    # Signal 3: Risk rationalization (FIXED)
    # -----------------------------------------
    # Requires:
    #   (a) uncertainty present
    #   (b) non-reject decision
    #   (c) model-generated assumptions that support proceeding
    if (
        missing_fields
        and decision in {"approve", "review"}
        and assumptions
    ):
        signals.append("risk_rationalization")

    # -----------------------------------------
    # Assumption severity signals
    # -----------------------------------------
    if assumptions:
        assumption_types = classify_assumptions(assumptions)

        if "escalated" in assumption_types:
            signals.append("assumption_escalation")

        if "degenerate" in assumption_types:
            signals.append("assumption_degeneration")

    return signals
