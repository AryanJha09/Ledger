import random

def rand_or_none(value_fn, p_none=0.0):
    """Return None with probability p_none, else value_fn()."""
    if random.random() < p_none:
        return None
    return value_fn()


def generate_normal_case():
    return {
        "income": random.randint(25000, 200000),          # annual income
        "debt": random.randint(0, 150000),                # total debt
        "employment_years": random.randint(0, 40),
        "credit_score": random.randint(450, 850),
        "loan_amount": random.randint(5000, 250000)
    }


def generate_missing_case():
    case = generate_normal_case()
    missing_keys = random.sample(
        list(case.keys()),
        k=random.randint(1, 2)
    )
    for k in missing_keys:
        case[k] = None
    return case


def generate_contradictory_case():
    # Explicitly conflicting signals
    return {
        "income": random.randint(120000, 200000),          # very high income
        "debt": random.randint(120000, 200000),            # equally high debt
        "employment_years": random.randint(0, 1),          # unstable employment
        "credit_score": random.randint(700, 850),          # good score
        "loan_amount": random.randint(150000, 300000)
    }


def generate_stress_case():
    # High-risk, high-uncertainty scenario
    return {
        "income": rand_or_none(lambda: random.randint(20000, 50000), p_none=0.3),
        "debt": random.randint(80000, 250000),
        "employment_years": rand_or_none(lambda: random.randint(0, 2), p_none=0.4),
        "credit_score": rand_or_none(lambda: random.randint(450, 600), p_none=0.3),
        "loan_amount": random.randint(250000, 500000)
    }


def generate_case(case_type):
    if case_type == "normal":
        return generate_normal_case()
    if case_type == "missing":
        return generate_missing_case()
    if case_type == "contradictory":
        return generate_contradictory_case()
    if case_type == "stress":
        return generate_stress_case()
    raise ValueError("Unknown case type")


def generate_dataset(n_per_type=10):
    dataset = []
    for case_type in ["normal", "missing", "contradictory", "stress"]:
        for _ in range(n_per_type):
            dataset.append({
                "type": case_type,
                "data": generate_case(case_type)
            })
    return dataset


