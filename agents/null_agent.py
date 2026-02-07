def run_null_agent(input_data):
    """
    Null epistemic baseline.
    Makes no assumptions, expresses neutral confidence,
    and defers decision.
    """
    return {
        "risks": [],
        "decision": "review",
        "confidence": 0.5,
        "assumptions": []
    }

