---
name: regression-diagnostics
description: Owns linear and logistic regression assumption checks, including diagnostics for outcome models fit after weighting or matching.
---

# Regression Diagnostics

## Scope

- This is the canonical skill for linear and logistic regression assumption checks.
- `analysis-hitl-plan` records which regression diagnostics are required versus recommended.
- `analysis-guardrails` enforces routing when those checks fail.
- It does not own method-specific estimand or design decisions for ITS/DID (see `quasi-experimental-its-did`) or IPTW (see `causal-iptw-weightit`); this skill supplies the outcome-model diagnostics those skills reference.

## Core decisions to confirm

- Purpose classification (descriptive, causal, or prediction), which changes the diagnostic emphasis.
- Functional form of continuous covariates: do not dichotomize continuous variables; allow non-linearity via splines or similar, consistent with `principles/compiled_principles.md`.

## Required checks (linear regression)

- Residual plots for linearity and homoscedasticity.
- Influential points (Cook's distance, leverage).
- Multicollinearity via VIF; report when VIF > 5, address when VIF > 10.

## Required checks (logistic regression)

- Linearity of the logit for continuous variables.
- Detection of complete or quasi-complete separation (confirm estimates are not diverging).
- Events-per-variable (EPV) check (guideline: EPV < 10 → state overfitting risk explicitly).
- Calibration via the Hosmer-Lemeshow test — use the same key as `code-review-companion`'s `assumption_checks` example: `hoslem_test`.

## Recommended checks

- Residual normality (relevant for inference in small samples).
- Discrimination (AUC) and internal validation, for prediction purposes.

## Implementation notes

- Use base R plus `car::vif()` and similar packages; guard every package with `requireNamespace()` and confirm with the user before installing anything missing.
- Do not finalize which diagnostics matter most, or how to resolve a failed check, on your own; present options and confirm with the user.
- Observational designs must not overstate causal claims; defer wording to `analysis-guardrails`.

## Handoff

- Also used for outcome-model diagnostics after IPTW weighting; this is referenced explicitly from `causal-iptw-weightit`.
- Also used for outcome-model diagnostics in ITS/DID segmented regressions; referenced from `quasi-experimental-its-did`.
- Record the agreed required and recommended checks in `analysis-hitl-plan` Gate 2B and Gate 2C.
