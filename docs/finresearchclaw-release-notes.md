# FinResearchClaw — Release Notes (Draft)

## Proposed fork name

**FinResearchClaw**

Why this name:
- preserves lineage with AutoResearchClaw / ResearchClaw
- short and easy to say
- broad enough for finance, accounting, and investment research
- specific enough to distinguish it from the generic upstream

## Positioning

FinResearchClaw is a finance/accounting/investment-specialized research pipeline derived from AutoResearchClaw.
It is intended for:
- finance research workflows
- accounting and reporting analysis
- investment and factor research
- event studies
- analyst forecast and valuation research

## What is new in this fork

### Domain layer
- Added `finance_accounting_investment` domain detection
- Added dedicated finance prompt adapter
- Added finance/accounting/investment keyword routing

### Prompting / pipeline behavior
- Finance-aware experiment-design overlays
- Finance-aware analysis overlays
- Finance-aware paper outline / draft / review / revision overlays
- Stronger bias checks for:
  - look-ahead bias
  - survivorship bias
  - leakage
  - implementation frictions

### Local data readiness
- Added `researchclaw/data/finance_local.py`
- Supports lightweight CSV/Parquet schema preview and finance dataset-type inference
- Documents recommended local data conventions for:
  - event studies
  - factor models
  - accounting panels
  - forecast error research

### Examples / starter templates
- `examples/finance_event_study.config.yaml`
- `examples/accounting_forecast_error.config.yaml`
- `examples/finance_event_study.exp_plan.yaml`
- `examples/factor_model_starter.exp_plan.yaml`
- `docs/finance-research-guide.md`

## Suggested GitHub repo name

- `FinResearchClaw`

## Suggested tagline

> Finance, accounting, and investment research automation on top of ResearchClaw.

## Suggested first release

- `v0.1.0-finance-preview`

## Suggested launch notes

This first finance preview focuses on domain detection, prompt specialization, local-data conventions, and starter templates. It does not yet bundle premium market-data connectors or production portfolio backtesting infrastructure.
