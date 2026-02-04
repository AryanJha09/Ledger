from pipeline.ingest import ingest_input
from pipeline.risk_assessment import assess_risk
from pipeline.decision_proposal import propose_decision
from pipeline.oversight import run_oversight
from pipeline.final_decision import finalize_decision


def run_pipeline(input_data):
    """
    Runs the full decision pipeline end-to-end and
    returns structured logs for diagnostics.
    """

    logs = {}

    # Stage 1: Ingest
    ingest_output = ingest_input(input_data)
    logs["ingest"] = ingest_output

    # Stage 2: Risk assessment
    risk_output = assess_risk(ingest_output)
    logs["risk_assessment"] = risk_output

    # Stage 3: Decision proposal
    proposal_output = propose_decision(risk_output)
    logs["proposal"] = proposal_output

    # Stage 4: Oversight
    oversight_output = run_oversight(ingest_output, proposal_output)
    logs["oversight"] = oversight_output

    # Stage 5: Final decision
    final_output = finalize_decision(proposal_output, oversight_output)
    logs["final"] = final_output

    return logs
