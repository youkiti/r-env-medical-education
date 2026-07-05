---
name: quasi-experimental-its-did
description: Owns ITS/DID-specific design choices, segmented-regression and parallel-trends diagnostics, and stability checks.
---

# Interrupted Time Series and Difference-in-Differences

## Scope

- This is the canonical skill for Interrupted Time Series (ITS) and Difference-in-Differences (DID) design decisions and diagnostics.
- `analysis-hitl-plan` records which ITS/DID checks are required versus recommended.
- `analysis-guardrails` enforces routing when those checks fail.
- It does not own general regression diagnostics (see `regression-diagnostics`) or missing-data handling (see `missing-data-mi`).

## Core decisions to confirm

- Design choice: single-group ITS, DID, or controlled ITS (CITS).
- Definition of the intervention time point: announcement vs implementation, and how any transition or phase-in period is handled.
- ITS parameterization: whether the primary estimand is a level change, a slope change, or both.
- DID group definition and unit of aggregation (individual, institution, or period).

## Required checks (ITS)

- Sufficient number of pre-intervention time points (guideline: at least 8 points on each side recommended; if fewer, state the limitation explicitly).
- Residual autocorrelation (Durbin-Watson test or residual ACF); if present, use a robust SE estimator such as Newey-West.
- Check for and address seasonality.
- Verify the segmented-regression specification (time, intervention, and time-after-intervention terms) against the approved plan.

## Required checks (DID)

- Parallel trends assessment: plotting pre-intervention trends is mandatory; test lead terms or an event-study specification when possible.
- Group composition stability (check for compositional change across periods).
- Consider anticipation effects (pre-intervention effect before the nominal intervention date).

## Recommended checks

- Placebo tests (fake intervention time or fake treatment group).
- Sensitivity analysis using different analysis windows.
- Wild cluster bootstrap when the number of clusters is small.

## Implementation notes

- Check packages with `requireNamespace()` before use. Base implementation is `lm()` plus `sandwich`/`lmtest` for Newey-West standard errors. For DID, prefer `fixest` when available; if it is not installed, confirm with the user before installing.
- Always output a plot of pre/post trends; follow the `reproducibility-standards` PNG+PDF export rule.
- This is an observational design; do not overstate causal claims on your own — defer causal wording to `analysis-guardrails`.
- Do not finalize the design choice, intervention time point, or estimand on your own; present options and confirm with the user.
- Reference `projects/medical_education_panel/` as a worked example of an ITS/DID handson.

## Handoff

- Record the agreed required and recommended ITS/DID checks in `analysis-hitl-plan` Gate 2B and Gate 2C.
- Route failed required checks back to model planning before interpretation.
