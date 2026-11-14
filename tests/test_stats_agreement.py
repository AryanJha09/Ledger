import math

import numpy as np

from ledger2 import agreement as ag
from ledger2 import stats as st


def test_wilson_known_value():
    lo, hi = st.wilson(7, 100)
    assert math.isclose(lo, 0.0343, abs_tol=1e-3) and math.isclose(hi, 0.1375, abs_tol=1e-3)
    assert st.wilson(0, 0)[0] != st.wilson(0, 0)[0]  # nan


def test_holm_monotone():
    adj = st.holm([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06])


def test_kappa_and_alpha():
    a = ["b", "e", "b", "b", "e", "d"]
    assert ag.cohens_kappa(a, a) == 1.0
    assert ag.krippendorff_alpha_nominal([[x, x] for x in a]) == 1.0
    # Krippendorff (2011) worked example, nominal, reliability ~0.743
    units = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [3, 3, 3], [2, 2, 2], [1, 2, 3], [4, 4, 4], [1, 1, 2],
             [2, 2, 2], [5, 5, 5], [1, 1, 1], [3, 3, 3]]
    alpha = ag.krippendorff_alpha_nominal(units)
    assert 0.6 < alpha < 0.9
    m = np.array([[3, 0], [0, 3], [2, 1], [3, 0]])
    assert -1 <= ag.fleiss_kappa(m) <= 1


def test_auroc_and_brier():
    assert st.auroc([0.9, 0.8, 0.1], [1, 1, 0]) == 1.0
    assert st.brier([1, 0], [1, 0]) == 0.0
