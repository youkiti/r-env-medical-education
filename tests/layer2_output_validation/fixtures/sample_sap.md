# Statistical Analysis Plan

## Document control

- Version: 1.0
- Date: 2026-03-01
- Author: Research Team

## Background

ChatGPT-4 has shown promise as a diagnostic support tool. This study evaluates its accuracy using standardized case vignettes.

## Objectives and hypotheses

- Primary: Estimate overall diagnostic accuracy of ChatGPT-4
- Secondary: Evaluate cognitive load and information quality

## Study design and data source

Cross-sectional diagnostic accuracy study. Data from 150 standardized clinical case vignettes.

## Study population

150 clinical case vignettes covering multiple medical specialties.

## Variables

- Primary outcome: answer_correct_bool (binary)
- Secondary: cognitive_load (ordinal 1-7), quality_answer (ordinal 1-5)
- Derived: diagnostic_result (TP/FP/TN/FN)

## Data processing plan

1. Import raw data from Excel
2. Validate variable types and ranges
3. Generate diagnostic accuracy matrix (TP/FP/TN/FN)

## Statistical principles

- Significance level: alpha = 0.05 (two-sided)
- Confidence intervals: 95% Wilson score intervals for proportions
- Multiple comparisons: Not applicable (single primary outcome)

## Descriptive and exploratory analyses

- Table 1: Case-level summary (N, %, mean, SD)
- Distribution plots for cognitive load and quality scores

## Primary analysis

- Sensitivity, Specificity, PPV, NPV with 95% CI
- ROC curve and AUC with DeLong CI
- Overall accuracy (proportion correct)

## Secondary analyses

- Mean cognitive load with 95% CI
- Mean quality score with 95% CI
- Correlation between cognitive load and accuracy

## Subgroup analyses

- Accuracy by medical specialty category (if available)

## Sensitivity analyses

- Exclude cases with fewer than 3 reviewers
- Alternative accuracy threshold (top-3 diagnosis match)

## Reproducibility and code operations

- All analyses in R 4.5.x
- renv for package management
- set.seed(123) for any random operations

## References

- DeLong et al. (1988) for AUC comparison
- STARD 2015 reporting guidelines

## Decision log

- Inter-rater reliability: Include as secondary analysis (Cohen's kappa) per intake open question
- Cognitive load threshold: Report descriptively, no pre-specified threshold
