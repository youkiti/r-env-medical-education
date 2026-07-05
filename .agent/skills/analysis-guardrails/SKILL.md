---
name: analysis-guardrails
description: Applies non-negotiable statistical rules and enforcement logic across analyses.
---

# Guardrails

## Scope

- This skill owns universal rules and escalation logic.
- It does not own model-specific checklists or data-cleaning procedures.

## Non-negotiable rules

- Do not fabricate results or claim significance without computed outputs.
- Do not assert causality in observational studies without stating assumptions and limitations.
- Do not rely on p-values alone; report estimates with 95% CI and exact p-values when available.
- Do not guess event coding; confirm categories from the data before modeling.
- Do not suppress warnings globally unless temporary and justified.

## Enforcement logic

- `data-wrangling` must be completed before interpretation-ready modeling starts.
- Custom helper functions must be tested before use in main analysis; use `tdd-testthat`.
- Required checks are always executed; failure returns the workflow to the approving Gate.
- Recommended checks are executed when their trigger occurs; results route to sensitivity or exploratory analysis unless the main specification must change.

## Interpretation rules

- Separate confirmatory, sensitivity, and exploratory findings in both code and reporting.
- State limitations when diagnostics are unavailable or optional packages are missing.
- Escalate unresolved statistical decisions back to the user instead of freezing them silently.

## Decisions requiring user confirmation

These can change results substantially. Present options with trade-offs and confirm before proceeding.

- Study-purpose classification (causal inference, descriptive association, or prediction).
- Distinction between primary/secondary outcomes and primary/sensitivity analyses (multiplicity handling).
- Missing-data handling (complete-case, multiple imputation, or another method); route to `missing-data-mi`.
- Handling of continuous variables (do not dichotomize by default; whether to allow non-linearity).
- Handling of clustering / repeated measures (mixed effects, robust SE, etc.).
- Variable selection (do not select on p-values alone; base it on prior knowledge).
- Causal wording in observational studies (avoid causal language; state assumptions).
- Propensity-score estimand (ATE/ATT) and trimming rules; route to `causal-iptw-weightit`.

## Safe defaults when unspecified

Low-risk steps that may proceed when the user has not specified otherwise.

- Start with overall/group-wise descriptive statistics via `tbl_summary()` (mean (SD), n (%), etc.).
- Center reporting on estimates with 95% CI; do not conclude from p-values alone (see `principles/compiled_principles.md`).
- Report exact p-values (for example `P = 0.043`), not `P < 0.05`.
- Set `set.seed(123)` whenever randomness is involved (sampling, splitting, imputation, etc.).
- For heavy or long analyses, verify behavior on a small sample before the full run.
- For large data, watch memory usage and start from column selection or aggregation (see `docs/summary.md`).

## Handoff

- Use method skills for model-specific check procedures.
- Use `analysis-hitl-plan` to record which checks are required versus recommended.
