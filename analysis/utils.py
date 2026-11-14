def is_tooling_failure(run):
    """
    Returns True if the run failed due to tooling or formatting issues,
    not due to model reasoning.

    Fix (v2 audit): run_experiment.py stores ``meta_error`` inside
    ``run["agent_output"]``, so the original top-level check never fired and
    parse failures were counted as model behaviour.
    """
    return "meta_error" in run or "meta_error" in run.get("agent_output", {})
