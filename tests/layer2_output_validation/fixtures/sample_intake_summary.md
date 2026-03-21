## Study Goal

Evaluate the diagnostic accuracy of ChatGPT-4 as a clinical decision-support tool for medical learners and clinicians.

## Design

Cross-sectional diagnostic accuracy study using 150 standardized clinical case vignettes.

## Outcome and Exposure

- Primary outcome: Diagnostic accuracy (correct/incorrect) of ChatGPT-4 responses
- Secondary outcomes: Cognitive load (7-point Likert), quality of medical information (5-point Likert)
- Exposure: ChatGPT-4 generated differential diagnosis vs. reference standard diagnosis

## Variables and Coding

- case_id: Unique case identifier (integer, 1-150)
- answer_correct_bool: Binary (TRUE/FALSE)
- cognitive_load: Ordinal (1-7)
- quality_answer: Ordinal (1-5)
- n_reviewers: Integer (2-4)
- diagnostic_result: Categorical (TP/FP/TN/FN)

## Missingness

- Expected missingness: <5% across all variables
- Mechanism: Assumed MCAR for reviewer non-response
- No exclusion rules based on missingness

## Reporting Needs

- Table 1: Case-level summary statistics
- Diagnostic accuracy metrics: Sensitivity, Specificity, PPV, NPV, AUC
- Figures: Accuracy bar chart, confusion matrix, ROC curve, cognitive load distribution, quality distribution
- Target journal: PLOS ONE format

## Additional Planning Inputs

- No custom helper functions expected initially
- No privacy constraints (synthetic data used)
- No causal estimand (descriptive study)

## Open Questions

- Should inter-rater reliability (Cohen's kappa) be included as a secondary analysis?
- What threshold defines "acceptable" cognitive load for clinical utility?
