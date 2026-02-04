import random

def run_mock_agent(input_data):
    """
    Simulates an LLM-based decision agent.
    This is intentionally imperfect and stochastic to expose pipeline failures.
    """

    risks = []

    # Simple risk heuristics (not meant to be correct)
    income = input_data.get("income")
    debt = input_data.get("debt")
    employment_years = input_data.get("employment_years")
    credit_score = input_data.get("credit_score")

    if debt is not None and debt > 80000:
        risks.append("high_debt")

    if employment_years is not None and employment_years < 2:
        risks.append("unstable_employment")

    if credit_score is not None and credit_score < 600:
        risks.append("low_credit_score")

    # Confidence is intentionally loosely coupled to risk
    confidence = round(random.uniform(0.6, 0.95), 2)

    # Decision logic (soft, inconsistent on purpose)
    if confidence > 0.75:
        decision = "approve"
    else:
        decision = "review"

    # Generate assumptions when information is missing
    assumptions = []
    if employment_years is None:
        assumptions.append("Assumed stable employment history")
    if income is None:
        assumptions.append("Assumed sufficient income")

    return {
        "risks": risks,
        "decision": decision,
        "confidence": confidence,
        "assumptions": assumptions
    }
