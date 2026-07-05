---
name: missing-data-mi
description: Owns the missing-data handling strategy decision and multiple imputation (MI) implementation and diagnostics.
---

# Missing Data and Multiple Imputation

## Scope

- This is the canonical skill for choosing a missing-data handling strategy and implementing multiple imputation (MI).
- Missingness diagnosis itself (quantifying and describing missingness) belongs to `data-wrangling` (Gate 0B); this skill owns everything from "how to handle it" onward.
- `analysis-hitl-plan` records which missing-data checks are required versus recommended.
- `analysis-guardrails` enforces routing when those checks fail.

## Core decisions to confirm

All of the following require explicit user confirmation; do not finalize any of them on your own.

- Assumed missingness mechanism (MCAR, MAR, or MNAR) and its justification.
- Conditions under which complete-case analysis is acceptable — only when missingness is minimal and MCAR is plausible, with the threshold agreed in advance.
- If performing MI: which variables to include in the imputation model (principle: include the outcome), and the number of imputations `m` (set according to the missingness fraction).

## Required checks

- Report the missingness fraction and missingness pattern per variable.
- Compare characteristics of groups with vs without missingness to assess whether missingness is informative.
- Confirm pooling is performed via Rubin's rules.
- Confirm convergence and distributional plausibility of imputations (trace plot, and comparison of imputed vs observed distributions).

## Recommended checks

- Compare complete-case vs MI results; record this comparison in Gate 2C as a sensitivity analysis.
- MNAR sensitivity analysis (for example, delta adjustment) as needed.

## Implementation notes

- `mice` is the first-choice package; check availability with `requireNamespace()`, and if it is missing, confirm with the user before installing.
- `set.seed(123)` is mandatory; save the imputation object for reproducibility.
- Verify behavior on synthetic data first, per `data-privacy-handling`.

## Handoff

- The missing-data strategy is documented in the SAP (`sap-authoring`) Data processing plan section.
- Record the agreed strategy and checks in `analysis-hitl-plan` Gate 0B (handling rule) and Gate 2C (sensitivity comparison).
