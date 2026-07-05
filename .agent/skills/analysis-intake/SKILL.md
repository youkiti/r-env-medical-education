---
name: analysis-intake
description: Collects study goals, design, variables, missingness, reporting needs, and open decisions before planning begins.
---

# Analysis Intake

## Scope

- Primary deliverable: `intake_summary.md` or an equivalent memo of confirmed facts and open questions.
- This skill collects information only.
- It does not write the SAP, assign Gate IDs, or prescribe code structure.

## Study framing

- Ask for the study goal and how the results will be used: descriptive, prognostic, prediction, causal, or exploratory.
- Ask for the study design, unit of analysis, and whether clustering or repeated measures exist.
- Ask whether the work is confirmatory or exploratory.

## Outcome and exposure

- Ask for outcome definition, timing, censoring rules, and event coding.
- Ask for exposure or intervention definition, index time, and whether it is time-varying.

## Variables and coding

- Ask for adjustment candidates and the rationale for inclusion or exclusion.
- Ask for coding details, units, legal ranges, and sentinel values.
- Ask about missingness amount, suspected mechanism, and known exclusion rules.

## Reporting needs

- Ask for target estimands or effect measures and required confidence intervals.
- Ask which tables and figures are expected: Table 1, regression tables, KM curves, balance plots, and similar outputs.
- Ask for a data dictionary or codebook and the data file location.

## Additional planning inputs

- Ask for planned sensitivity analyses and exploratory analyses, but record them as requirements rather than deciding the final plan here.
- Ask whether custom helper functions are expected; if yes, flag `tdd-testthat`.
- Ask for privacy or governance constraints; if yes, flag `data-privacy-handling`.
- Ask whether a causal estimand and propensity-score workflow are intended; if yes, flag `causal-iptw-weightit`.
- Ask whether a quasi-experimental design (ITS/DID) is intended; if yes, flag `quasi-experimental-its-did`.
- Ask whether missingness is expected to be non-negligible; if yes, flag `missing-data-mi`.

## When the user is undecided

- If the user is unsure how to proceed, first produce descriptive statistics, a missingness summary, and simple visualizations, then move on to modeling.

## Handoff

- Pass confirmed facts and unresolved questions to `sap-authoring`.
- Keep unresolved items explicit; do not silently fill gaps.
