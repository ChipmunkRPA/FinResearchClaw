"""Finance/accounting/investment domain prompt adapter.

Provides domain-specific prompt blocks for finance, accounting,
and investment research workflows.
"""

from __future__ import annotations

from typing import Any

from researchclaw.domains.prompt_adapter import PromptAdapter, PromptBlocks


class FinancePromptAdapter(PromptAdapter):
    """Adapter for finance, accounting, and investment domains."""

    def get_code_generation_blocks(self, context: dict[str, Any]) -> PromptBlocks:
        domain = self.domain

        return PromptBlocks(
            compute_budget=domain.compute_budget_guidance or (
                "Finance/accounting experiments are CPU-friendly. Focus on multiple "
                "specifications, robust inference, and robustness checks rather than "
                "heavy model training."
            ),
            dataset_guidance=domain.dataset_guidance or (
                "Use synthetic or user-provided firm-level panel data with dates, "
                "identifiers, returns, statement variables, and event markers. "
                "Avoid live downloads in main.py."
            ),
            hp_reporting=domain.hp_reporting_guidance or (
                "Report research-design parameters in HYPERPARAMETERS, for example: "
                "{'n_firms': ..., 'n_periods': ..., 'event_window': ..., "
                "'lookback': ..., 'winsor_pct': ..., 'factor_set': ...}"
            ),
            code_generation_hints=domain.code_generation_hints or self._default_hints(),
            output_format_guidance=self._output_format(),
        )

    def get_experiment_design_blocks(self, context: dict[str, Any]) -> PromptBlocks:
        domain = self.domain

        design_context = (
            f"This is a **{domain.display_name}** experiment.\n"
            "Paradigm: progressive benchmark → enriched specification → robustness checks.\n\n"
            "Key principles for finance/accounting/investment experiments:\n"
            "1. Start with accepted benchmark models (CAPM, FF3/FF5, naive forecast, base panel regression).\n"
            "2. Add controls, fixed effects, event windows, or factor extensions progressively.\n"
            "3. Separate statistical significance from economic significance.\n"
            "4. Audit look-ahead bias, survivorship bias, and leakage explicitly.\n"
            "5. Include at least one robustness or placebo test and one subsample analysis.\n"
        )

        return PromptBlocks(
            experiment_design_context=design_context,
            statistical_test_guidance=(
                "Use robust or clustered standard errors, Newey-West where serial correlation "
                "matters, Hausman tests for panel choices, and placebo / alternative-window tests "
                "for event studies."
            ),
        )

    def get_result_analysis_blocks(self, context: dict[str, Any]) -> PromptBlocks:
        return PromptBlocks(
            result_analysis_hints=(
                "Finance/accounting result analysis:\n"
                "- Report both economic magnitude and statistical significance\n"
                "- Compare benchmark alpha / explanatory power / forecast error across specifications\n"
                "- Check robustness by period, industry, firm size, and event window\n"
                "- Discuss data leakage, look-ahead bias, and survivorship bias risks\n"
                "- For portfolio results, report turnover and implementation frictions if relevant"
            ),
            statistical_test_guidance=(
                "Use robust, clustered, or Newey-West inference as appropriate; report t-stats, "
                "confidence intervals, and placebo/sensitivity outcomes."
            ),
        )

    def _default_hints(self) -> str:
        return (
            "Finance/accounting code requirements:\n"
            "1. Build a dated panel with firm identifiers and clearly lagged features\n"
            "2. Implement benchmark model(s) first, then enriched and robustness specifications\n"
            "3. Support event-study, forecasting, or factor-model workflows as appropriate\n"
            "4. Report table-ready outputs with coefficients, t-stats, R², alpha, forecast errors, or CARs\n"
            "5. Save structured results to results.json with metadata about windows, factors, and sample filters\n"
        )

    def _output_format(self) -> str:
        return (
            "Output structured finance/accounting results to results.json:\n"
            '{"specifications": {\n'
            '    "benchmark": {"alpha": 0.01, "t_stat": 2.1, "n": 5000},\n'
            '    "full_spec": {"alpha": 0.015, "t_stat": 2.8, "n": 5000}\n'
            '  },\n'
            '  "metadata": {"domain": "finance_accounting_investment", "event_window": "[-1,+1]"}}'
        )
