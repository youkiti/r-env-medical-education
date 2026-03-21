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

## Handoff

- Use method skills for model-specific check procedures.
- Use `analysis-hitl-plan` to record which checks are required versus recommended.
