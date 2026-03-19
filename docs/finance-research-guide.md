# Finance / Accounting / Investment Research Guide

This fork now includes a domain layer for finance, accounting, and investment research.

## What it changes

When the topic looks like finance/accounting/investment research, the pipeline now biases toward:

- benchmark-first experiment design
- event-study and factor-model style comparisons
- accounting panel-regression workflows
- finance-style outputs such as alpha, CAR/BHAR, forecast error, and regression tables
- stronger warnings around:
  - look-ahead bias
  - survivorship bias
  - leakage
  - implementation frictions

## Example topics

- Event study of abnormal returns around earnings announcements
- Accrual quality and analyst forecast error
- Fama-French factor model for portfolio alpha
- Bankruptcy risk prediction from financial statement signals
- Valuation error analysis using accounting ratios

## Domain conventions

### Typical baselines

- CAPM
- Fama-French 3-factor
- Fama-French 5-factor
- analyst-consensus benchmark
- naive persistence forecast
- fixed effects panel regression

### Typical outputs

- regression tables
- factor exposure tables
- event-study tables
- coefficient plots
- cumulative abnormal return plots
- forecast error plots

## Current design philosophy

This extension does **not** assume live WRDS / Compustat / CRSP / Capital IQ access.
Instead, it steers the pipeline to:

1. use user-provided data when available, or
2. generate realistic synthetic firm-level panels for method development and dry runs.

That keeps the framework usable in local sandbox environments.

## Example configs and starter templates

See:

- `examples/finance_event_study.config.yaml`
- `examples/accounting_forecast_error.config.yaml`
- `examples/finance_event_study.exp_plan.yaml`
- `examples/factor_model_starter.exp_plan.yaml`

## Local data conventions (CSV / Parquet)

Recommended local dataset layout:

- `data/finance/events.csv` or `.parquet`
- `data/finance/factors.csv` or `.parquet`
- `data/finance/accounting_panel.csv` or `.parquet`

Recommended columns by family:

- **Event study**: `date`, `firm_id`, `ret`, `event_date`, `mkt_rf`, `rf`
- **Factor model**: `date`, `ret`, `rf`, `mkt_rf`, `smb`, `hml` (+ `rmw`, `cma` if available)
- **Accounting panel**: `firm_id`, `date`/`fyear`, `assets`, `sales`, `accruals`, `earnings`
- **Forecast error**: `forecast`, `actual`, `forecast_error`, `analyst_count`, `consensus`

Helper module:

- `researchclaw/data/finance_local.py`

It provides lightweight schema inference and CSV/Parquet preview support for local finance datasets.

## Notes for production-grade finance research

If you later want to push this beyond domain prompting and into a more specialized finance workflow, the next natural upgrades are:

- explicit event-window parameterization
- portfolio sort and rebalancing logic
- transaction cost / turnover modeling
- Newey-West and clustered inference defaults
- local-data connectors for WRDS-style or internal parquet/CSV datasets
