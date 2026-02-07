def is_tooling_failure(run):
    """
    Returns True if the run failed due to tooling or formatting issues,
    not due to model reasoning.
    """
    return "meta_error" in run

