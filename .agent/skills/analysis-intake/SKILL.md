---
name: analysis-intake
description: Collects study goals, design, variables, missingness, and reporting needs before starting clinical epidemiology analysis.
---

# Analysis Intake

## Study Design and Goals

- Ask for the study goal and how results will be used (descriptive, prognostic, prediction, causal, exploratory).
- Ask for study design and unit of analysis; confirm independence, clustering, or repeated measures.

## Outcome and Exposure

- Ask for outcome definition: type, timing, censoring rules, and event coding meaning.
- Ask for exposure or intervention definition, start time, and whether it is time-varying.

## Variables and Coding

- Ask for adjustment candidates and the rationale for including or excluding variables.
- Ask for variable coding details (0/1 meaning), units, and sentinel values (e.g., 999).
- Ask about missingness amount, suspected mechanism, and exclusion criteria.

## Reporting Needs

- Ask for reporting needs: effect measure, 95% CI, and expected tables or figures (Table 1, regression tables, KM curves, balance plots).
- Ask for a data dictionary or codebook and the data file location.

## Sensitivity and Exploratory Analysis

- Ask for sensitivity analysis approach:
  - Outlier exclusion criteria (e.g., ±3SD)
  - Alternative model specifications
  - Complete case vs imputation comparison
- Ask for exploratory analysis plans:
  - Stratified analyses (e.g., by sex, age group)
  - Interaction terms to explore
  - Subgroup hypotheses (label as exploratory)

## Technical Requirements

- Ask for unit testing needs: will custom functions be created? If so, define test cases.

> [!TIP]
> テスト実装の詳細は `tdd-testthat` スキルを参照。

- Ask for version control requirements: R version, key package versions to document.
