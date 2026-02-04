def ingest_input(input_data):
    """
    Ingests raw applicant data and records missing fields.
    Does not modify the data.
    """

    missing_fields = []
    for key, value in input_data.items():
        if value is None:
            missing_fields.append(key)

    return {
        "data": input_data,
        "missing_fields": missing_fields,
        "missing_count": len(missing_fields)
    }
