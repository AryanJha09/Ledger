def finalize_decision(proposal_output, oversight_output):
    """
    Produces the final decision.
    Oversight signals are intentionally not enforced.
    """

    return {
        "final_decision": proposal_output["proposed_decision"],
        "confidence": proposal_output["confidence"],
        "assumptions": proposal_output["assumptions"],
        "oversight_flags": oversight_output["flags"]
    }
