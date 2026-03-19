"""Local finance/accounting dataset helpers.

Utilities for working with local CSV/Parquet datasets in finance-oriented
research runs. This module is intentionally lightweight:
- CSV works with Python stdlib only
- Parquet is supported when pandas is available
- schema detection is heuristic, not opinionated magic
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

CANONICAL_FINANCE_COLUMNS: dict[str, tuple[str, ...]] = {
    "panel_core": (
        "date", "firm_id", "ticker", "gvkey", "permno", "cusip",
        "industry", "sic", "fyear", "fqtr",
    ),
    "market": (
        "ret", "excess_ret", "mkt_rf", "smb", "hml", "rmw", "cma", "rf",
        "volume", "turnover", "market_cap", "price",
    ),
    "accounting": (
        "assets", "sales", "revenue", "ni", "earnings", "accruals",
        "book_equity", "debt", "cash", "cfo", "roe", "roa",
    ),
    "events": (
        "event_date", "announcement_date", "filing_date", "window_start",
        "window_end", "car", "bhar", "surprise",
    ),
    "forecasts": (
        "forecast", "actual", "forecast_error", "analyst_count",
        "consensus", "dispersion",
    ),
}

FINANCE_DATASET_PATTERNS: dict[str, tuple[str, ...]] = {
    "event_study": (
        "event_date", "announcement_date", "car", "bhar", "surprise",
    ),
    "factor_model": (
        "ret", "excess_ret", "mkt_rf", "smb", "hml", "rmw", "cma", "rf",
    ),
    "accounting_panel": (
        "firm_id", "gvkey", "fyear", "fqtr", "assets", "sales", "accruals",
    ),
    "forecast_error": (
        "forecast", "actual", "forecast_error", "analyst_count", "consensus",
    ),
}


def normalize_columns(columns: list[str]) -> list[str]:
    return [c.strip().lower().replace(" ", "_") for c in columns]


def infer_finance_dataset_kind(columns: list[str]) -> str:
    """Infer a dataset family from column names.

    Returns one of: event_study, factor_model, accounting_panel,
    forecast_error, mixed_finance_panel, unknown.
    """
    normalized = set(normalize_columns(columns))

    # Event-study data often includes factor columns too; event markers should win.
    if {"event_date", "announcement_date", "car", "bhar", "surprise"} & normalized:
        if {"date", "ret", "firm_id"} & normalized:
            return "event_study"

    # Forecast-error research should also outrank generic panel matching.
    if {"forecast", "actual", "forecast_error", "consensus"} & normalized:
        return "forecast_error"

    best_name = "unknown"
    best_score = 0
    for name, patterns in FINANCE_DATASET_PATTERNS.items():
        score = sum(1 for p in patterns if p in normalized)
        if score > best_score:
            best_name = name
            best_score = score
    if best_score >= 2:
        return best_name
    if ({"date", "firm_id"} & normalized) and ({"ret", "assets", "sales"} & normalized):
        return "mixed_finance_panel"
    return "unknown"


def finance_schema_summary(columns: list[str]) -> dict[str, Any]:
    normalized = normalize_columns(columns)
    column_set = set(normalized)
    coverage = {
        group: sorted([c for c in expected if c in column_set])
        for group, expected in CANONICAL_FINANCE_COLUMNS.items()
    }
    return {
        "dataset_kind": infer_finance_dataset_kind(normalized),
        "columns": normalized,
        "coverage": coverage,
        "has_date": "date" in column_set or "event_date" in column_set,
        "has_firm_key": any(k in column_set for k in ("firm_id", "ticker", "gvkey", "permno")),
    }


def read_tabular_preview(path: str | Path, max_rows: int = 5) -> dict[str, Any]:
    """Read a lightweight preview of a CSV or Parquet file.

    Parquet requires pandas to be installed in the active environment.
    """
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        with p.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames or [])
            rows = []
            for i, row in enumerate(reader):
                rows.append(row)
                if i + 1 >= max_rows:
                    break
        return {
            "path": str(p),
            "format": "csv",
            "columns": normalize_columns(fieldnames),
            "preview_rows": rows,
            "schema": finance_schema_summary(fieldnames),
        }
    if suffix in {".parquet", ".pq"}:
        try:
            import pandas as pd  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Parquet preview requires pandas") from exc
        df = pd.read_parquet(p)
        fieldnames = [str(c) for c in df.columns.tolist()]
        return {
            "path": str(p),
            "format": "parquet",
            "columns": normalize_columns(fieldnames),
            "preview_rows": df.head(max_rows).to_dict(orient="records"),
            "schema": finance_schema_summary(fieldnames),
        }
    raise ValueError(f"Unsupported tabular format: {p.suffix}")


def recommended_research_conventions(dataset_kind: str) -> list[str]:
    if dataset_kind == "event_study":
        return [
            "Use explicit event windows such as [-1,+1], [-3,+3], and [0,+1].",
            "Report CAR or BHAR with benchmark return model stated explicitly.",
            "Run placebo or alternative-window sensitivity checks.",
        ]
    if dataset_kind == "factor_model":
        return [
            "Benchmark against CAPM, FF3, and FF5 where applicable.",
            "Report alpha, factor loadings, t-stats, and sample period clearly.",
            "Check turnover and implementation frictions for portfolio claims.",
        ]
    if dataset_kind == "forecast_error":
        return [
            "Lag features carefully to avoid look-ahead bias.",
            "Report MAE/RMSE and benchmark against naive persistence or consensus.",
            "Stratify by period, industry, and firm size where feasible.",
        ]
    if dataset_kind == "accounting_panel":
        return [
            "Prefer progressive specifications: base regression, controls, fixed effects, robustness.",
            "Winsorization and missing-data handling should be stated explicitly.",
            "Discuss economic magnitude, not only p-values.",
        ]
    return [
        "State identifier keys, date conventions, and lag logic explicitly.",
        "Audit look-ahead bias, survivorship bias, and leakage before drawing conclusions.",
    ]
