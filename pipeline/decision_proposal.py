def propose_decision(risk_output):
    """
    Proposes a decision based on agent risk output.
    This is intentionally simple and does not resolve uncertainty.
    """

    decision = risk_output["agent_output"].get("decision")

    return {
        "proposed_decision": decision,
        "confidence": risk_output["confidence"],
        "assumptions": risk_output["assumptions"],
        "risks": risk_output["risks"]
    }
