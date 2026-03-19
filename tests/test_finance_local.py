from __future__ import annotations

from pathlib import Path

from researchclaw.data.finance_local import (
    finance_schema_summary,
    infer_finance_dataset_kind,
    read_tabular_preview,
    recommended_research_conventions,
)


def test_infer_event_study_kind():
    cols = ["date", "firm_id", "ret", "event_date", "mkt_rf", "rf", "car"]
    assert infer_finance_dataset_kind(cols) == "event_study"


def test_infer_factor_model_kind():
    cols = ["date", "ret", "rf", "mkt_rf", "smb", "hml", "rmw", "cma"]
    assert infer_finance_dataset_kind(cols) == "factor_model"


def test_finance_schema_summary_flags_keys():
    summary = finance_schema_summary(["Date", "Ticker", "Assets", "Sales", "Forecast_Error"])
    assert summary["has_date"] is True
    assert summary["has_firm_key"] is True


def test_read_csv_preview(tmp_path: Path):
    path = tmp_path / "sample.csv"
    path.write_text(
        "date,firm_id,ret,event_date,mkt_rf,rf\n"
        "2024-01-01,A,0.01,2024-01-02,0.005,0.0001\n",
        encoding="utf-8",
    )
    preview = read_tabular_preview(path)
    assert preview["format"] == "csv"
    assert preview["schema"]["dataset_kind"] == "event_study"
    assert preview["preview_rows"]


def test_recommended_conventions_for_forecast_error():
    recs = recommended_research_conventions("forecast_error")
    joined = " ".join(recs).lower()
    assert "look-ahead bias" in joined
    assert "mae/rmse" in joined
