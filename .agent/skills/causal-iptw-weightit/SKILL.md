---
name: causal-iptw-weightit
description: Owns IPTW-specific estimand, weighting, balance, and stability guidance using WeightIt.
---

# IPTW with WeightIt

## Scope

- This is the canonical skill for IPTW-specific diagnostics and stability checks.
- `analysis-hitl-plan` records which IPTW checks are required versus recommended.
- `analysis-guardrails` enforces routing when those checks fail.

## Core decisions to confirm

- Target estimand: ATE, ATT, or another estimand.
- Propensity-score specification and covariate set.
- Stabilization and trimming rules.
- Outcome model after weighting, if any.

## Required checks

- Positivity and overlap: inspect propensity-score distributions by treatment group.
- Weight distribution: report min, max, quantiles, and the presence of extreme weights.
- Effective sample size: report ESS and interpret large drops as instability signals.
- Balance diagnostics: report standardized mean differences and aim for SMD < 0.1 unless otherwise approved.

## Recommended checks

- Trimming sensitivity analyses with alternative thresholds.
- Alternative propensity-score model specifications.
- Doubly robust analysis when pre-agreed or triggered by instability concerns.

## Implementation notes

- Use `WeightIt` instead of `iptw`; see `docs/iptw_note.md`.
- Use `summary(<weightit object>)` and `cobalt::bal.tab()` or `cobalt::love.plot()` when available.
- Report instability risks explicitly and avoid overstating causal claims.

## Handoff

- Record the agreed required and recommended IPTW checks in `analysis-hitl-plan` Gate 2B and Gate 2C.
- Route failed required checks back to model planning before interpretation.
