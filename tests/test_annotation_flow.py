import numpy as np

from ledger2 import agreement, annotation


def test_annotation_round_trip(fake_runs, tmp_path):
    sheet, key = annotation.build(fake_runs, 20)
    assert "model_key" not in sheet.columns and "v2_label" not in sheet.columns  # blinded
    key_path = tmp_path / "key.csv"
    key.to_csv(key_path, index=False)
    rng = np.random.default_rng(1)
    files = []
    for name in ("ann_a", "ann_b", "ann_c"):
        s = sheet.copy()
        # stand-in labels: copy the v2 label with some noise
        s["label"] = [v if rng.random() > 0.2 else "benign" for v in key.v2_label]
        p = tmp_path / f"{name}.csv"
        s.to_csv(p, index=False)
        files.append(p)
    rep = agreement.run(files, key_path, tmp_path / "val")
    assert rep["n_items"] == len(sheet) and rep["fleiss_kappa"] is not None
    assert "v2_label" in rep and (tmp_path / "val" / "agreement.json").exists()
