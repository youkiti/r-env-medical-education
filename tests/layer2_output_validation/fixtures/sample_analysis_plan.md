# Analysis Plan: ChatGPT Diagnostic Study

## Gate 0A: Environment Setup

- G0A-1: Verify R version >= 4.5.0
- G0A-2: Verify renv lockfile and restore packages
- G0A-3: Verify data file accessibility

## Gate 0B: Data Preparation

- G0B-1: Import raw Excel data
- G0B-2: Validate variable types and ranges
- G0B-3: Generate diagnostic accuracy matrix (TP/FP/TN/FN)
- G0B-4: Export cleaned dataset with cleaning log

## Gate 1: Exploration

- G1-1: Generate Table 1 (case-level summary statistics)
- G1-2: Distribution plots for cognitive load and quality scores
- G1-3: Verify overall accuracy against published value (49.3%)

## Gate 2A: Descriptive Analysis

- G2A-1: Compute diagnostic accuracy metrics (sensitivity, specificity, PPV, NPV)
- G2A-2: Report all metrics with 95% Wilson score CI

## Gate 2B: Primary Analysis

- G2B-1: ROC curve generation
- G2B-2: AUC computation with DeLong CI
- G2B-3: Overall accuracy with exact binomial CI

## Gate 2C: Sensitivity Analysis

- G2C-1: Exclude cases with fewer than 3 reviewers and re-compute metrics
- G2C-2: Top-3 diagnosis match alternative accuracy

## Gate 2D: Exploratory Analysis

- G2D-1: Inter-rater reliability (Cohen's kappa)
- G2D-2: Correlation between cognitive load and accuracy
