---
name: analysis-guardrails
description: Applies statistical guardrails, required checks, and non-negotiable prohibitions for clinical epidemiology analyses.
---

# Guardrails

- Do not fabricate results or claim significance without computed outputs.
- Do not assert causality in observational studies; state assumptions and limitations.
- Do not rely on p-values alone; report estimates with 95% CI and exact p-values.
- Do not guess event coding; confirm actual categories with `table()` before modeling.
- Do not suppress warnings (e.g., `options(warn = -1)`) unless temporary and justified.

## Required checks before modeling

> [!NOTE]
> これらのチェックは `data-wrangling` スキルのステップ完了後に実施。

- Confirm row counts and event counts for primary outcomes.
- Check variable types (numeric, factor, date) and units.
- Summarize missingness by column and for key variables.
- Scan for impossible values (e.g., age < 0, extreme BMI, sentinel codes).

## Required checks for custom functions

- If custom functions are created, write unit tests using `testthat` or equivalent.
- Test edge cases: missing data, empty inputs, boundary values.
- Document test results before using functions in main analysis.

> [!TIP]
> 詳細なTDD手順・テンプレートは `tdd-testthat` スキルを参照。

## Model assumption check enforcement

- Model assumption checks are governed by Gate 2B agreement.
- **必須チェック**: Always perform. If NG, do not proceed to interpretation. Return to Gate 2B.
- **推奨チェック**: Perform when pre-agreed triggers occur. Route results to Gate 2C.

### Package availability

The following packages enhance assumption checks but are not mandatory:
- `car` (VIF calculation) — if unavailable, compute manually or note limitation
- `survminer` (cox.zph visualization) — prefer ggplot-based outputs when available; if unavailable, use base `plot()`
- `performance` (model diagnostics) — optional enhancement

Before using these packages, check availability:

```r
if (requireNamespace("car", quietly = TRUE)) {
  car::vif(model)
} else {
  message("car package not available; VIF check skipped or use manual calculation")
}
```

### Model-specific checks quick reference

| Model Type | 必須チェック | 推奨チェック |
|------------|-------------|-------------|
| Linear Regression | Linearity, Homoscedasticity, Residual normality | VIF |
| Logistic Regression | Outcome coding, Convergence/separation, Influential points | Linearity in logit, Calibration |
| Cox Regression | Proportional hazards (`cox.zph()`) | Functional form, Influential points |
| IPTW | PS overlap, Weight distribution, Balance (SMD) | Trimming sensitivity, Double robust |

## Default low-risk workflow

- Start with descriptive summaries (e.g., `tbl_summary()` overall or by group).
- Summarize missingness and simple visualizations before modeling.
- Use `set.seed(123)` for any random operations.
- Use a small subset to confirm code runs before full analysis.

## References

- Read `principles/compiled_principles.md` for statistical principles.
