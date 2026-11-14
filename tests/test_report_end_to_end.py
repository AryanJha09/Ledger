from ledger2.report import build_report


def test_report_builds_from_logs(fake_runs, tmp_path):
    md = build_report(fake_runs, tmp_path / "report")
    text = md.read_text()
    assert "Format compliance" in text and "Wilson" in text
    assert (tmp_path / "report" / "t1_signals_loan.tex").exists()
    assert (tmp_path / "report" / "fig_unsupported_by_condition_loan.pdf").exists()
    assert "t9_consistency" in {p.stem for p in (tmp_path / "report").iterdir()}
