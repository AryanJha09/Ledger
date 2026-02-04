def run_oversight(ingest_output, proposal_output):
    """
    Performs a lightweight oversight check.
    Flags risks, missing information, and assumption usage.
    Does NOT enforce changes.
    """

    flags = []

    # Flag missing information
    if ingest_output["missing_count"] > 0:
        flags.append("missing_information")

    # Flag detected risks
    if len(proposal_output["risks"]) > 0:
        flags.append("risk_detected")

    # Flag use of assumptions
    if len(proposal_output["assumptions"]) > 0:
        flags.append("assumptions_used")

    return {
        "flags": flags,
        "flag_count": len(flags)
    }
